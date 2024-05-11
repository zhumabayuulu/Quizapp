from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    bio = models.CharField(max_length=100, null=True, blank=True)
    pic = models.ImageField(upload_to='profiles/', default="profiles/male-avatar-maker.jpg")
    is_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

