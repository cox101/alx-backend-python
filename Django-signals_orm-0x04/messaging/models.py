from django.db import models
from chats.models import User
from .managers import UnreadMessagesManager

class Message(models.Model):

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    # a parent_message field (self-referential foreign key) to represent replies.
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    # conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # Custom manager for unread messages
    # class Meta:
    #     ordering = ['-sent_at']
    #     indexes = [
    #         models.Index(fields=['conversation', 'sent_at']),
    #         models.Index(fields=['sender']),
    #     ]
    
    def __str__(self):
        return f"Message from {self.sender} in {self.conversation}"

class Notification(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient} regarding message {self.message.message_id}"


class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    edited_at = models.DateTimeField(auto_now=True)
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='edited_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for message {self.message.id} at {self.timestamp}"
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['message', 'timestamp']),
        ]