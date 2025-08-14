#!/usr/bin/env python
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import MessagePagination


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['participants']
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MessageFilter
    pagination_class = MessagePagination
    ordering_fields = ['timestamp']

    def get_queryset(self):
        # Only return messages where the user is a participant in the conversation
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation')
        if conversation and self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant of this conversation.")
        serializer.save(sender=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user not in instance.conversation.participants.all():
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user not in instance.conversation.participants.all():
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user not in instance.conversation.participants.all():
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
