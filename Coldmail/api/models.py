from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.postgres.search import SearchVector, SearchVectorField  # Added for full-text search
from django.contrib.postgres.indexes import GinIndex  # Added for full-text search index

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

class HistoryEntry(models.Model):
    TONE_CHOICES = [
        ('formal', 'Formal'),
        ('friendly', 'Friendly'),
        ('bold', 'Bold'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history_entries')
    created_at = models.DateTimeField(default=timezone.now)
    resume_file_name = models.CharField(max_length=255)
    resume_content = models.TextField()
    target_company = models.CharField(max_length=255)
    role_applied_for = models.CharField(max_length=255)
    tone = models.CharField(max_length=20, choices=TONE_CHOICES)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    
    # Full-text search field
    search_vector = SearchVectorField(null=True, blank=True)

    def __str__(self):
        return f"{self.target_company} - {self.role_applied_for}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update search vector
        HistoryEntry.objects.filter(pk=self.pk).update(
            search_vector=SearchVector(
                'target_company',
                'role_applied_for',
                'tone',
                'subject',
                'body',
                'resume_file_name'
            )
        )

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "History Entries"
        indexes = [
            GinIndex(fields=['search_vector'])  # Create GIN index for faster search
        ]