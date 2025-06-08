from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS # Importing SAFE_METHODS to allow read-only access

class IsOwnerOrParticipant(permissions.BasePermission):
    """
    Custom permission to only allow users to access objects (messages/conversations)
    they own or participate in.
    """

    def has_object_permission(self, request, view, obj):
        # For messages: user must be sender or receiver
        if hasattr(obj, 'sender') and hasattr(obj, 'receiver'):
            return obj.sender == request.user or obj.receiver == request.user

        # For conversations: user must be in participants list (assuming many-to-many)
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        return False
    def has_permission(self, request, view):
        # Allow access if the user is authenticated
        return request.user and request.user.is_authenticated or request.method in permissions.SAFE_METHODS
        # Allow safe methods (GET, HEAD, OPTIONS) for unauthenticated users
        # This allows read-only access to conversations/messages without authentication
        # return request.method in permissions.SAFE_METHODS or request.user and request.user.is_authenticated
    def has_permission(self, request, view):    
        # Allow access if the user is authenticated
        return request.user and request.user.is_authenticated or request.method in permissions.SAFE_METHODS
    
    

class IsParticipantOfConversation(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS include GET, HEAD, OPTIONS
        if hasattr(obj, 'conversation'):
            participants = obj.conversation.participants.all()
            return request.user in participants
        return False
