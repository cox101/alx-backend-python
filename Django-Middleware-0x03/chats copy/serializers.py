#!/usr/bin/env python
from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_username', 'conversation', 'content', 'timestamp']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages', 'created_at']

    def get_messages(self, obj):
        messages = obj.message_set.all().order_by('timestamp')
        return MessageSerializer(messages, many=True).data

    def validate(self, data):
        participants = self.initial_data.get('participants')
        if not participants or len(participants) < 2:
            raise serializers.ValidationError("At least two participants are required for a conversation.")
        return data


