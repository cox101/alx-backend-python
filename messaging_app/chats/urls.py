#!/usr/bin/env python
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

nested_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
]
# This code sets up nested routing for the messaging app, allowing messages to be accessed within the context of a specific conversation.
# The `NestedDefaultRouter` is used to create a nested route for messages under conversations, enabling cleaner and more organized API endpoints.