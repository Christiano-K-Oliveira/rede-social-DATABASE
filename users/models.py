from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=150)
    username = models.CharField(max_length=80, unique=True, error_messages={"unique": "A user with that username already exists."})
    email = models.EmailField(max_length=127, unique=True, error_messages={"unique": "This field must be unique."})
    password = models.CharField(max_length=127)
    birthdate = models.DateField(null=True)
    bio = models.TextField(max_length=300)

    def __str__(self) -> str:
        return f'<UserId {self.id} - Email: {self.email}, Username: {self.username}>'
