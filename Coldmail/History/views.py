from rest_framework import generics, permissions
from .models import History
from .serializers import HistorySerializer

class HistoryListCreateView(generics.ListCreateAPIView):
    serializer_class = HistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return History.objects.filter(user=self.request.user).order_by('-created_at')

class HistoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return History.objects.filter(user=self.request.user)
# history/urls.py
from django.urls import path
from .views import HistoryListCreateView, HistoryDetailView

urlpatterns = [
    path('', HistoryListCreateView.as_view(), name='history-list'),
    path('<int:pk>/', HistoryDetailView.as_view(), name='history-detail'),
]
