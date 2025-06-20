from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  GeminiMailDetailWithResumesView, UserMailHistoryView, GenerateAndSaveMailView, DeleteMailHistoryView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    # JWT token endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain'),  # POST: {username, password}
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # POST: {refresh}

    # Custom endpoints
    path('gemini-mail/<str:id>/', GeminiMailDetailWithResumesView.as_view(), name='gemini-mail-detail'),  # GET: Retrieve a specific mail and its resumes by GeminiMail ID
    path('mail-history/', UserMailHistoryView.as_view(), name='mail-history'),  # GET: Get all mail history for the authenticated user
    path('generate-mail/', GenerateAndSaveMailView.as_view(), name='generate-mail'),  # POST: {file, target_role, target_company, tone} - Generate mail and save resume/mail
    path('delete-mail-history/<str:id>/', DeleteMailHistoryView.as_view(), name='delete-mail-history'),  # DELETE: Delete a mail history by GeminiMail ID
]

