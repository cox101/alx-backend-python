from rest_framework import permissions

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