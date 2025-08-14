#!/usr/bin/env python
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
# Import custom view for extended token functionality
from chats.auth import CustomTokenObtainPairView


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/', include('chats.urls')),
    
    path('api-auth/', include('rest_framework.urls')),
    path('api-auth/', include('rest_framework.authtoken.urls')),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]