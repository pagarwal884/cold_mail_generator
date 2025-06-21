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
            resumes = ResumeData.objects.filter(gemini_mail=gemini_mail, user=request.user)
            for resume in resumes:
                data.append({
                    'gemini_id': gemini_mail.id,
                    'resume_file': resume.file.url if resume.file else '',
                    'target_company': resume.target_company,
                    'target_role': resume.target_role,
                    'resume_name': resume.resume_name,
                    'resume_content': resume.resume_content,
                    'tone': resume.tone,
                    'subject': gemini_mail.subject,
                    'body': gemini_mail.body,
                    'timestamp': int(resume.created_at.timestamp() * 1000) if hasattr(resume, 'created_at') and resume.created_at else None
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
        resume_content = request.data.get('resume_content', None)
        resume_name = request.data.get('resume_name', None)
        user = request.user

        if not all([target_role, target_company, tone, resume_content, resume_name]):
            return Response({'error': 'All fields are required.'}, status=400)

        # Generate mail using Gemini
        subject, body = generate_cold_mail_gemini_api(resume_content, target_company, target_role, tone)

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
                file=file,
                resume_content=resume_content,
                resume_name=resume_name
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

class ParseResumeView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided.'}, status=400)
        try:
            resume_content = parse_resume(file)
            resume_name = file.name
            return Response({'resume_content': resume_content, 'resume_name': resume_name}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)





