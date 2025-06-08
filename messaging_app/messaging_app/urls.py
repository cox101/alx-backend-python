#!/usr/bin/env python
from django.contrib import admin
from django.urls import path, include
from messaging_app.chats import auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),  # Include your app's routes
    path('api-auth/', include('rest_framework.urls')),  # Enable browsable API login/logout
        path('admin/', admin.site.urls),
    path('api/auth/', include(auth)),            # JWT auth endpoints: /api/auth/token/, /api/auth/token/refresh/
    path('api/chats/', include('messaging_app.chats.urls')),  # Your chat app API endpoints
]
# This code sets up the main URL configuration for the Django project, including the admin interface and API routes for the messaging app.
# It includes the admin site and the API routes defined in the `chats` app, allowing for easy access to the messaging functionality.