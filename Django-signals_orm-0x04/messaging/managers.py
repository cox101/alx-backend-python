from django.db import models

class UnreadMessagesManager(models.Manager):
    
    def unread_for_user(self, user):
        """
        Custom manager method to retrieve unread messages for a specific user.
        """
        return self.filter(receiver=user, read=False).only('content', 'timestamp', 'sender')
    
    def mark_as_read(self, message_ids):
        """
        Custom manager method to mark messages as read.
        """
        return self.filter(id__in=message_ids).update(read=True)