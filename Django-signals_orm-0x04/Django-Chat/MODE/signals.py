from django.dispatch import Signal
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory



@receiver(post_save, sender=Message)
def message_sent(sender, instance, created, **kwargs):
    if created:
        print(f"Message sent: {instance.content} by {instance.sender} to {instance.receiver}")


@receiver(post_save, sender=Message)
def notification_created(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(message=instance, recipient=instance.receiver)
        print(f"Notification created for message: {instance.content} sent by {instance.sender} to {instance.receiver}")

@receiver(pre_save, sender=Message)
def message_edited(sender, instance, **kwargs):
    if instance.pk:
        original = Message.objects.get(pk=instance.pk)
        if original.content != instance.content:
            instance.edited = True
            MessageHistory.objects.create(message=original, content=original.content)
            print(f"Message edited: {instance.content} by {instance.sender} to {instance.receiver}")
        else:
            instance.edited = False