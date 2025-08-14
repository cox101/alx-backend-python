from django.db import models
from chats.models import User

class Message(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    edited = models.BooleanField(default=False)

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
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for message {self.message.id} at {self.timestamp}"
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['message', 'timestamp']),
        ]