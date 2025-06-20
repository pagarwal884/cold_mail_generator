from django.db import models
from django.conf import settings
from django_nanoid.models import NANOIDField
import os

class GeminiMail(models.Model):
    id = NANOIDField(primary_key=True, max_length=21, secure_generated=True, editable=False, unique=True)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Mail - {self.subject}"

class ResumeData(models.Model):
    id = NANOIDField(primary_key=True, max_length=21, secure_generated=True, editable=False, unique=True)
    TONE_CHOICES = [
        ('Formal', 'Formal'),
        ('Casual', 'Casual'),
        ('Persuasive', 'Persuasive'),
        ('Concise', 'Concise'),
        ('Enthusiastic', 'Enthusiastic'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gemini_mail = models.ForeignKey(GeminiMail, on_delete=models.CASCADE, related_name='resumes')
    target_company = models.CharField(max_length=255)
    target_role = models.CharField(max_length=255)
    tone = models.CharField(max_length=20, choices=TONE_CHOICES)
    file = models.FileField(upload_to='resume_files/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.target_company} - {self.target_role} ({self.user.username})"

    def delete(self, *args, **kwargs):
        # Delete the file from storage if it exists
        if self.file and self.file.name and os.path.isfile(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)

