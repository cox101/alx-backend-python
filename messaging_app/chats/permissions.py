from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to view, send, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Only allow authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Ensure object has a conversation attribute
        if hasattr(obj, 'conversation'):
            participants = obj.conversation.participants.all()

            # Check if user is a participant
            if request.user not in participants:
                return False

            # Allow all safe methods (GET, HEAD, OPTIONS)
            if request.method in SAFE_METHODS:
                return True

            # Allow PUT, PATCH, DELETE only for participants
            if request.method in ['PUT', 'PATCH', 'DELETE']:
                return True

        return False
    def has_permission(self, request, view):
        # Allow access to authenticated users
        return request.user and request.user.is_authenticated