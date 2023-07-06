from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    registered_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

class UserLoginRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"

@receiver(user_logged_in)
def record_user_login(sender, user, request, **kwargs):
    UserLoginRecord.objects.create(user=user)
