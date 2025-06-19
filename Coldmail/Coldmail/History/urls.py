from django.urls import path
from .views import HistoryListCreateView, HistoryDetailView
from .views_2 import GenerateMailView

urlpatterns = [
    path('', HistoryListCreateView.as_view(), name='history-list'),
    path('<int:pk>/', HistoryDetailView.as_view(), name='history-detail'),
    path('generate/', GenerateMailView.as_view(), name='generate-mail'),
]
