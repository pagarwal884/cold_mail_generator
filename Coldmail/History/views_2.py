from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .services import parse_resume, generate_cold_mail
from .serializers import HistorySerializer
import logging

logger = logging.getLogger(__name__)

class GenerateMailView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            job_desc = request.data.get('job_description')
            tone = request.data.get('tone', 'professional')
            resume_file = request.FILES.get('resume')
            
            if not job_desc:
                return Response({'error': 'Job description is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            resume_text = ""
            if resume_file:
                resume_text = parse_resume(resume_file)
            
            subject, body = generate_cold_mail(job_desc, resume_text, tone)
            
            # Save to history
            history_data = {
                'job_description': job_desc,
                'generated_subject': subject,
                'generated_body': body,
            }
            serializer = HistorySerializer(data=history_data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response({
                'subject': subject,
                'body': body,
                'history_id': serializer.data['id']
            })
        
        except Exception as e:
            logger.error(f"Error generating email: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
