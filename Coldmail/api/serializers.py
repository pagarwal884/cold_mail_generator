from rest_framework import serializers
from .models import Resume, ColdEmail, HistoryEntry
from django.contrib.auth import get_user_model

User = get_user_model()

class HistoryEntrySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)  # Use UUIDField if your IDs are UUIDs
    resumeFileName = serializers.CharField(source='resume_file_name')
    resumeContent = serializers.CharField(source='resume_content')
    targetCompany = serializers.CharField(source='target_company')
    roleAppliedFor = serializers.CharField(source='role_applied_for')
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    user = serializers.PrimaryKeyRelatedField(  # Add user field
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = HistoryEntry
        fields = [
            'id', 
            'user',
            'resumeFileName', 
            'resumeContent', 
            'targetCompany', 
            'roleAppliedFor', 
            'tone', 
            'subject', 
            'body', 
            'createdAt'
        ]
        read_only_fields = ['id', 'createdAt', 'user']  # Make these fields read-only

class ResumeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, 
        default=serializers.CurrentUserDefault()
    )
    
    class Meta:
        model = Resume
        fields = ['id', 'user', 'file', 'extracted_text', 'created_at', 'updated_at']
        read_only_fields = ['id', 'extracted_text', 'created_at', 'updated_at', 'user']

class ColdEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColdEmail
        fields = [
            'id',
            'resume',
            'generated_content',
            'prompt_used',
            'recipient_email',
            'subject_line',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'generated_content']  # Add generated_content to read-only