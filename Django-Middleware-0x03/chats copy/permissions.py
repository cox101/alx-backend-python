from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation to:
    - View the conversation/messages (safe methods: GET, HEAD, OPTIONS)
    - Send, update, or delete messages (POST, PUT, PATCH, DELETE)
    """

    def has_permission(self, request, view):
        # Only allow authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if the object is related to a conversation
        if not hasattr(obj, 'conversation'):
            return False
            
        # Get conversation participants
        participants = obj.conversation.participants.all()
        
        # User must be a participant
        if request.user not in participants:
            return False
            
        # For safe methods, allow access
        if request.method in SAFE_METHODS:
            return True
            
        # For unsafe methods (POST, PUT, PATCH, DELETE), also allow access
        # Note: POST typically handled by has_permission, not has_object_permission
        return True