#!/usr/bin/env python
from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User model
class User(AbstractUser):
    # You can extend with additional fields here if needed
    # e.g., phone_number = models.CharField(max_length=15, blank=True)
    pass


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        participant_usernames = ", ".join([user.username for user in self.participants.all()])
        return f"Conversation between: {participant_usernames}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"
