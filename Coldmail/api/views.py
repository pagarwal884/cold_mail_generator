from rest_framework import viewsets, permissions
from .models import Resume, ColdEmail
from .serializers import ResumeSerializer, ColdEmailSerializer

class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ColdEmailViewSet(viewsets.ModelViewSet):
    queryset = ColdEmail.objects.all()
    serializer_class = ColdEmailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(resume__user=self.request.user)