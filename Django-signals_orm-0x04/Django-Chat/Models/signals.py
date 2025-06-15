from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory
from django.db.models.signals import post_delete
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.id:
        try:
            original = Message.objects.get(pk=instance.id)
            if original.content != instance.content:
                MessageHistory.objects.create(
                    message=original,
                    old_content=original.content
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass  # Message is new, no edit yet


@receiver(post_delete, sender=User)
def delete_related_data(sender, instance, **kwargs):
    # Delete messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications associated with the user
    Notification.objects.filter(user=instance).delete()

    # Delete message histories associated with messages sent or received by the user
    MessageHistory.objects.filter(
        message__sender=instance
    ).delete()
    MessageHistory.objects.filter(
        message__receiver=instance
    ).delete()
