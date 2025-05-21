from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from app.utils import TelegramUserManager


class TelegramUser(AbstractBaseUser, PermissionsMixin):

    id = models.BigIntegerField(unique=True, primary_key=True, null=False, blank=False)
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    language_code = models.CharField(max_length=10)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = []

    password = models.CharField(max_length=128, default=UNUSABLE_PASSWORD_PREFIX)
    objects = TelegramUserManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"@{self.username}" or f"ID-{str(self.id)}"

class Task(models.Model):

    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, max_length=500)
    due_date = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    reminder_sent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({'✓' if self.is_completed else '✗'})"

class Remainder(models.Model):

    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='reminders')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='reminders')
    time = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user}: ({self.task.title})"