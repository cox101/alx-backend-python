#!/usr/bin/env python
from rest_framework import viewsets
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets 
from rest_framework.response import Response

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['participants']

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['conversation', 'sender']
    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')
        if conversation_id:
            return self.queryset.filter(conversation__id=conversation_id)
        return self.queryset
    
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


