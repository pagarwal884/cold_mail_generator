from rest_framework import serializers
from .models import ResumeData, GeminiMail


class ResumeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeData
        fields = ['id', 'file', 'target_company', 'target_role', 'tone']

class GeminiMailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeminiMail
        fields = ['id', 'subject', 'body']
