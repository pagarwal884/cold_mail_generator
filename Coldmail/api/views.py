from rest_framework import viewsets, permissions
from .models import Resume, ColdEmail, HistoryEntry
from .serializers import ResumeSerializer, ColdEmailSerializer, HistoryEntrySerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import models  # Import models for Q objects

class HistoryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get search parameter
        search_term = request.query_params.get('search', '').strip()
        
        # Start with user's history
        history = HistoryEntry.objects.filter(user=request.user).order_by('-created_at')
        
        # Apply search filter if term exists using Q objects
        if search_term:
            history = history.filter(
                models.Q(target_company__icontains=search_term) |
                models.Q(role_applied_for__icontains=search_term) |
                models.Q(tone__icontains=search_term) |
                models.Q(subject__icontains=search_term) |
                models.Q(body__icontains=search_term) |
                models.Q(resume_file_name__icontains=search_term)
            )
        
        serializer = HistoryEntrySerializer(history, many=True)
        return Response(serializer.data)

class HistoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, entry_id):
        entry = get_object_or_404(HistoryEntry, id=entry_id, user=request.user)
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ColdEmailViewSet(viewsets.ModelViewSet):
    queryset = ColdEmail.objects.all()
    serializer_class = ColdEmailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(resume__user=self.request.user)