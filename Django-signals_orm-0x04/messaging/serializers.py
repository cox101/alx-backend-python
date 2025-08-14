from rest_framework import serializers
from .models import Message, Notification, MessageHistory

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'content', 'timestamp', 'sender', 'receiver', 'edited']
        read_only_fields = ['timestamp', 'edited']
        extra_kwargs = {
            'sender': {'read_only': True},
            'receiver': {'read_only': True}
        }
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'recipient', 'read', 'timestamp']
        read_only_fields = ['timestamp']
        extra_kwargs = {
            'message': {'read_only': True},
            'recipient': {'read_only': True}
        }
class MessageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageHistory
        fields = ['id', 'message', 'content', 'timestamp']
        read_only_fields = ['timestamp']
        extra_kwargs = {
            'message': {'read_only': True}
        }