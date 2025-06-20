from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResumeViewSet, ColdEmailViewSet, HistoryListView, HistoryDetailView  # Added missing imports
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'resumes', ResumeViewSet, basename='resume')
router.register(r'cold-emails', ColdEmailViewSet, basename='coldemail')

urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('history/', HistoryListView.as_view(), name='history-list'),
    path('history/<uuid:entry_id>/', HistoryDetailView.as_view(), name='history-detail'),
]