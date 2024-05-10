from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    bio = models.CharField(max_length=100, null=True, blank=True)
    pic = models.ImageField(upload_to='profiles/', default="profiles/avatar.svg")
    is_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)


# contact form
class ContactForm(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    message = models.TextField(max_length=500)

    def __str__(self):
        return self.email