from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Override only to enforce uniqueness (already unique in AbstractUser, but explicit here)
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    # All other fields from AbstractUser are inherited