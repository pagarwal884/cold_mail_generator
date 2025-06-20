from rest_framework import generics
from .models import ResumeData, GeminiMail
from .serializers import ResumeDataSerializer, GeminiMailSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .services import parse_resume, generate_cold_mail_gemini_api
from django.db import transaction

class GeminiMailDetailWithResumesView(generics.RetrieveAPIView):
    queryset = GeminiMail.objects.all()
    serializer_class = GeminiMailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        gemini_mail = self.get_object()
        gemini_mail_serialized = GeminiMailSerializer(gemini_mail).data
        resumes = ResumeData.objects.filter(gemini_mail=gemini_mail)
        resumes_serialized = ResumeDataSerializer(resumes, many=True).data
        return Response({
            'gemini_mail': gemini_mail_serialized,
            'resumes': resumes_serialized
        })

class UserMailHistoryView(generics.ListAPIView):
    serializer_class = GeminiMailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get all GeminiMail objects that have at least one resume for the current user
        return GeminiMail.objects.filter(resumes__user=self.request.user).distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = []
        for gemini_mail in queryset:
            gemini_mail_serialized = GeminiMailSerializer(gemini_mail).data
            resumes = ResumeData.objects.filter(gemini_mail=gemini_mail, user=request.user)
            resumes_serialized = ResumeDataSerializer(resumes, many=True).data
            data.append({
                'gemini_mail': gemini_mail_serialized,
                'resumes': resumes_serialized
            })
        return Response(data)

class GenerateAndSaveMailView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        target_role = request.data.get('target_role')
        target_company = request.data.get('target_company')
        tone = request.data.get('tone')
        user = request.user

        if not all([file, target_role, target_company, tone]):
            return Response({'error': 'All fields are required.'}, status=400)

        # Parse resume file
        resume_text = parse_resume(file)

        # Generate mail using Gemini
        subject, body = generate_cold_mail_gemini_api(resume_text, target_company, target_role, tone)

        with transaction.atomic():
            # Save GeminiMail
            gemini_mail = GeminiMail.objects.create(subject=subject, body=body)
            # Save ResumeData
            resume_data = ResumeData.objects.create(
                user=user,
                gemini_mail=gemini_mail,
                target_company=target_company,
                target_role=target_role,
                tone=tone,
                file=file
            )
        return Response({
            'resume': ResumeDataSerializer(resume_data).data,
            'gemini_mail': GeminiMailSerializer(gemini_mail).data
        }, status=201)

class DeleteMailHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id, *args, **kwargs):
        try:
            gemini_mail = GeminiMail.objects.get(id=id)
            # Only allow deletion if the user owns at least one resume linked to this mail
            if not ResumeData.objects.filter(gemini_mail=gemini_mail, user=request.user).exists():
                return Response({'error': 'Not authorized to delete this mail history.'}, status=403)
            gemini_mail.delete()
            return Response({'message': 'Mail history deleted successfully.'}, status=204)
        except GeminiMail.DoesNotExist:
            return Response({'error': 'Mail history not found.'}, status=404)





