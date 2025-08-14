from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets
from .models import Message, Notification, MessageHistory
from .serializers import MessageSerializer, NotificationSerializer, MessageHistorySerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from chats.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_unread_messages(self, request, *args, **kwargs):
        """
        Retrieve unread messages for the authenticated user.
        """
        user = request.user
        unread_messages = Message.objects.filter(receiver=user, read=False)
        serializer = self.get_serializer(unread_messages, many=True)
        return Response(serializer.data)
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class MessageHistoryViewSet(viewsets.ModelViewSet):
    """
    Display the message edit history in the user interface, allowing users to view previous versions of their messages.
    """
    queryset = MessageHistory.objects.all()
    serializer_class = MessageHistorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

def delete_user(request, user_id):
    """
    Delete a user and all their messages, notifications, and message history.
    """
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return render(request, 'success.html', {'message': 'User and related data deleted successfully.'})
    except User.DoesNotExist:
        return render(request, 'error.html', {'message': 'User not found.'})
    except Exception as e:
        return render(request, 'error.html', {'message': str(e)})


@method_decorator(cache_page(60), name='dispatch')
def unread_messages_view(request):
    # Get unread messages for the current user
    unread_messages = Message.unread.unread_for_user(request.user)\
                        .only('content', 'timestamp', 'sender')\
                        .select_related('sender')
    
    replies = Message.objects.filter(sender=request.user)\
                    .only('content', 'timestamp', 'sender')\
                    .select_related('reply_to')\
                    .prefetch_related('replies')
    context = {
        'unread_messages': unread_messages,
        'replies': replies
    }
    return render(request, 'messages/unread.html', context)
def replies_view(request, message_id):
    """
    View to display replies to a specific message.
    """
    try:
        sender = Q(sender=request.user)
        message = Message.objects.filter(id=message_id, sender=sender).select_related('sender').first()
        if not message:
            return render(request, 'error.html', {'message': 'Message not found or you do not have permission to view it.'})
        replies = Message.objects.prefetch_related('replies')
        
        context = {
            'message': message,
            'replies': replies
        }
        return render(request, 'messages/replies.html', context)
    except Message.DoesNotExist:
        return render(request, 'error.html', {'message': 'Message not found.'})