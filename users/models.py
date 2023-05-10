from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # Include any additional fields or methods as needed

    def __str__(self):
        return self.username
