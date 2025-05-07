from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    verification_code = models.CharField(max_length=64, blank=True, null=True)
