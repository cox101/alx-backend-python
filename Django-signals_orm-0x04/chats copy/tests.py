from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import User, Conversation, Message

class MessagingTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Create test users
        self.user1 = User.objects.create_user(email="user1@example.com", password="pass123")
        self.user2 = User.objects.create_user(email="user2@example.com", password="pass123")

        # Authenticate user1
        self.client.force_authenticate(user=self.user1)

        # Create a conversation
        self.conversation = Conversation.objects.create()
        self.conversation.participants.set([self.user1, self.user2])

        # Create a message
        self.message = Message.objects.create(
            sender=self.user1,
            conversation=self.conversation,
            message_body="Hello there!"
        )

    def test_conversation_creation(self):
        response = self.client.post(
            reverse('conversation-list'),
            data={'participants': [self.user1.id, self.user2.id]},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('participants', response.data)

    def test_send_message(self):
        response = self.client.post(
            reverse('message-list'),
            data={
                'conversation': str(self.conversation.conversation_id),
                'message_body': "Test message",
                'sender': str(self.user1.user_id)
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message_body'], "Test message")

    def test_get_conversations(self):
        response = self.client.get(reverse('conversation-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_messages(self):
        response = self.client.get(reverse('message-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
