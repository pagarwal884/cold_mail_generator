from rest_framework import serializers
from .models import Resume, ColdEmail

class ResumeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, 
        default=serializers.CurrentUserDefault()
    )
    
    class Meta:
        model = Resume
        fields = ['id', 'user', 'file', 'extracted_text', 'created_at', 'updated_at']
        read_only_fields = ['extracted_text', 'created_at', 'updated_at']

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
        read_only_fields = ['created_at']