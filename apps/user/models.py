from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum

class RoleChoices(Enum):
    USER = 'user'
    ADMIN = 'admin'
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    role = models.CharField(max_length=10, choices=[(role.value, role.name) for role in RoleChoices], default=RoleChoices.USER.value)

    def __str__(self):
        return self.email

