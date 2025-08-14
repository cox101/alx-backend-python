from datetime import datetime, timedelta
from collections import defaultdict
import threading
from django.http import HttpResponseForbidden, JsonResponse
from rest_framework import status
from rest_framework.response import Response
# from django.conf import settings
from os import path


class RequestLoggingMiddleware:
    """
    Middleware to log the request method and path.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log the request method and path
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        file_name = path.join(path.dirname(__file__), 'requests.log')
        # Log the request details to a file named 'requests.log'
        with open(file_name, 'a') as log_file:
            log_file.write(f"{datetime.now()} - User: {user} - Path: {request.path}\n")
        
        # Call the next middleware or view
        response = self.get_response(request)
        
        return response

class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access between specified hours with configurable time windows.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_start = 18  # 6 PM
        self.allowed_end = 21     # 9 PM

    def __call__(self, request):
        current_hour = datetime.now().hour
        
        if not (self.allowed_start <= current_hour < self.allowed_end):
            return JsonResponse(
                {
                    "error": "Access restricted",
                    "message": f"Access is only allowed between {self.allowed_start}:00 and {self.allowed_end}:00",
                    "current_time": datetime.now().strftime("%H:%M")
                },
                status=403
            )
        
        return self.get_response(request)

class OffensiveLanguageMiddleware:
    """
    Rate limiting middleware with improved IP handling and thread safety.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_counts = defaultdict(list)
        self.limit = 5
        self.time_window = 60  # seconds

    def __call__(self, request):
        if request.method == 'POST':
            ip_address = self._get_client_ip(request)
            current_time = datetime.now()

            with threading.Lock():  # Ensure thread safety
                self._clean_old_entries(ip_address, current_time)
                
                if len(self.message_counts[ip_address]) >= self.limit:
                    return self._rate_limit_response(ip_address)
                
                self.message_counts[ip_address].append(current_time)

        return self.get_response(request)

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

    def _clean_old_entries(self, ip_address, current_time):
        self.message_counts[ip_address] = [
            ts for ts in self.message_counts[ip_address]
            if (current_time - ts).seconds < self.time_window
        ]

    def _rate_limit_response(self, ip_address):
        oldest = min(self.message_counts[ip_address])
        retry_after = (oldest + timedelta(seconds=self.time_window) - datetime.now()).seconds
        return JsonResponse(
            {
                "error": "Rate limit exceeded",
                "message": f"Maximum {self.limit} messages per {self.time_window} seconds allowed",
                "retry_after": retry_after
            },
            status=429,
            headers={'Retry-After': str(retry_after)}
        )

class RolepermissionMiddleware:
    """
    Role-based access control middleware with configurable permissions.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_paths = ["/api/v1/conversations","/api/v1/messages", "/auth/", "/api-auth/"]
        self.allowed_roles =  ['admin', 'moderator']

    def __call__(self, request):
        if any(request.path.startswith(path) for path in self.exempt_paths):
            return self.get_response(request)

        if not request.user.is_authenticated:
            return self._unauthorized_response()

        user_role = self._get_user_role(request.user)
        
        if user_role not in self.allowed_roles:
            return self._forbidden_response(user_role)

        return self.get_response(request)

    def _get_user_role(self, user):
        if hasattr(user, 'profile'):
            return user.profile.role
        return getattr(user, 'role', None)

    def _unauthorized_response(self):
        return JsonResponse(
            {
                "error": "Authentication required",
                "message": "Please log in to access this resource"
            },
            status=401
        )

    def _forbidden_response(self, user_role):
        return JsonResponse(
            {
                "error": "Permission denied",
                "message": f"Your role '{user_role}' doesn't have access to this resource",
                "required_roles": self.allowed_roles
            },
            status=status.HTTP_403_FORBIDDEN
        )