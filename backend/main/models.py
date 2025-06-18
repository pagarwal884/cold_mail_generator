from django.db import models
from base.models import Basemodel
from django.contrib.auth.hashers import make_password

class CustomUser(Basemodel):
    mail = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)


class ResumeFile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    processed_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.file.name} ({'processed' if self.processed else 'unprocessed'})"


class ColdMail(Basemodel):
    gen_response = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.ForeignKey(ResumeFile, on_delete=models.CASCADE)

    def __str__(self):
        return f"ColdMail {self.id} for User {self.user.username}"
