from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessagingSignalTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='alice', password='password')
        self.receiver = User.objects.create_user(username='bob', password='password')

    def test_notification_created_on_message(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Hello, Bob!'
        )
        notification = Notification.objects.filter(message=message, user=self.receiver).first()
        self.assertIsNotNone(notification)
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.is_read)  