
from django.contrib import admin
from .models import CustomUser, ContactForm


# Register your models here.
admin.site.register(CustomUser)

admin.site.register(ContactForm)