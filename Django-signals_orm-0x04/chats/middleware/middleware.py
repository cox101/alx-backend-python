import logging
from datetime import timedelta
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        logger.info(f"{timezone.now()} - User: {user} - Path: {request.method} {request.path}")
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_start = getattr(settings, 'ACCESS_START_HOUR', 18)  # 6 PM
        self.allowed_end = getattr(settings, 'ACCESS_END_HOUR', 21)      # 9 PM

    def __call__(self, request):
        current_hour = timezone.now().hour
        if not (self.allowed_start <= current_hour < self.allowed_end):
            return JsonResponse(
                {
                    "error": "Access restricted",
                    "message": f"Access is only allowed between {self.allowed_start}:00 and {self.allowed_end}:00",
                    "current_time": timezone.now().strftime("%H:%M")
                },
                status=403
            )
        return self.get_response(request)


class RateLimitingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.limit = getattr(settings, 'RATE_LIMIT', 5)
        self.time_window = getattr(settings, 'RATE_WINDOW', 60)  # seconds

    def __call__(self, request):
        if request.method == 'POST':
            ip = self._get_client_ip(request)
            cache_key = f"rate:{ip}"
            current_count = cache.get(cache_key, 0)

            if current_count >= self.limit:
                retry_after = cache.ttl(cache_key)
                return JsonResponse(
                    {
                        "error": "Rate limit exceeded",
                        "message": f"Max {self.limit} POSTs per {self.time_window}s",
                        "retry_after": retry_after
                    },
                    status=429,
                    headers={'Retry-After': str(retry_after)}
                )

            if current_count == 0:
                cache.set(cache_key, 1, timeout=self.time_window)
            else:
                cache.incr(cache_key)

        return self.get_response(request)

    def _get_client_ip(self, request):
        x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        return x_forwarded.split(",")[0] if x_forwarded else request.META.get("REMOTE_ADDR")


class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_paths = ["/api/v1/conversations", "/api/v1/messages", "/auth/", "/api-auth/"]
        self.allowed_roles = ['admin', 'moderator']

    def __call__(self, request):
        if any(request.path.startswith(path) for path in self.exempt_paths):
            return self.get_response(request)

        if not request.user.is_authenticated:
            return JsonResponse(
                {
                    "error": "Authentication required",
                    "message": "Please log in to access this resource"
                },
                status=401
            )

        user_role = self._get_user_role(request.user)
        if user_role not in self.allowed_roles:
            return JsonResponse(
                {
                    "error": "Permission denied",
                    "message": f"Your role '{user_role}' doesn't have access to this resource",
                    "required_roles": self.allowed_roles
                },
                status=status.HTTP_403_FORBIDDEN
            )

        return self.get_response(request)

    def _get_user_role(self, user):
        if hasattr(user, 'profile'):
            return user.profile.role
        return getattr(user, 'role', None)