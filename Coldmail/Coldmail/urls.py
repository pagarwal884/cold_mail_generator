# Coldmail/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('Account.urls')),
    path('api/', include('api.urls')),
]

# Health check endpoint
if hasattr(settings, 'HEALTH_CHECK_PATH'):
    from django.http import HttpResponse
    urlpatterns += [
        path(settings.HEALTH_CHECK_PATH, lambda r: HttpResponse(status=200))
    ]