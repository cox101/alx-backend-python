
from django.contrib.auth import authenticate
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import LoginSerializer

# from .models import User, Conversation, Message
from .serializers import LoginSerializer, UserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
 # Import JWT view for token issuance
from rest_framework_simplejwt.views import TokenObtainPairView
 # Import typing for type annotations
from typing import Dict, Any


class AuthViewSet(viewsets.ViewSet):  # Changed from ModelViewSet to ViewSet
    """
    Custom authentication endpoints that return user data along with tokens.
    """
    serializer_class = LoginSerializer
    permission_classes = []  # No permissions required for login
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        Custom login that returns both token and user data.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            request=request,
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        
        if not user:
            return Response(
                {'error': 'Invalid Credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        })
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """
        Custom logout that clears the token.
        """
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()
        return Response({'status': 'logged out'})

 # Customize token serializer to include additional user data
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user) -> Dict[str, Any]:
        # Get base token with standard claims (e.g., user_id)
        token = super().get_token(user)
        # Add username to token payload for client-side use
        token['email'] = user.email # Alternative: Add roles or email
        # Return modified token
        return token

 # Custom view to use the extended serializer
class CustomTokenObtainPairView(TokenObtainPairView):
    # Link serializer to handle custom token generation
    serializer_class = CustomTokenObtainPairSerializer