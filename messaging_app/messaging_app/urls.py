#!/usr/bin/env python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),  # Include your app's routes
    path('api-auth/', include('rest_framework.urls')),  # Enable browsable API login/logout
]
# This code sets up the main URL configuration for the Django project, including the admin interface and API routes for the messaging app.
# It includes the admin site and the API routes defined in the `chats` app, allowing for easy access to the messaging functionality.