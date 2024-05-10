from django.contrib import admin

# Register your models here.
from .models import *


class QuestionInline(admin.TabularInline):
    model = Question


class TestAdmin(admin.ModelAdmin):
    inlines = [QuestionInline, ]
    list_display = ['title', 'author']


# test

admin.site.register([TestCategory, Question]),
admin.site.register(Test, TestAdmin),
admin.site.register([CheckTest,CheckQuestion])

# endtest