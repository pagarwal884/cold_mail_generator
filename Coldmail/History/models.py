from django.db import models
from Account.models import User

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_description = models.TextField()
    generated_subject = models.CharField(max_length=255)
    generated_body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

