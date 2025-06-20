from rest_framework import serializers
from .models import ResumeData, GeminiMail


class ResumeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeData
        fields = '__all__'

class GeminiMailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeminiMail
        fields = '__all__'
