from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Resume(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='resumes'
    )
    file = models.FileField(upload_to='resumes/')  # Store PDF/DOCX files
    extracted_text = models.TextField(blank=True)  # Extracted text from resume
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resume {self.id} - {self.user.username}"

class ColdEmail(models.Model):
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='cold_emails'
    )
    generated_content = models.TextField()  # Gemini-generated email
    prompt_used = models.TextField()  # Prompt sent to Gemini
    created_at = models.DateTimeField(default=timezone.now)
    
    # Additional metadata
    recipient_email = models.EmailField()
    subject_line = models.CharField(max_length=255)
    generation_parameters = models.JSONField(default=dict)  # Temp, tokens, etc.

    def __str__(self):
        return f"Cold Email for Resume {self.resume.id}"