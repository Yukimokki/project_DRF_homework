from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {"blank": True, "null": True}

class User(AbstractUser):
    username = models.CharField(max_length=35, verbose_name="user_name", **NULLABLE, help_text="name")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=35, verbose_name="phone_number", **NULLABLE, help_text="phone number")
    city = models.CharField(max_length=50, verbose_name="telegram_name", **NULLABLE, help_text="your Telegram name")
    avatar = models.ImageField(upload_to="users/avatars", verbose_name="Avatar", **NULLABLE, help_text="User picture")

    token = models.CharField(max_length=100, verbose_name="Token", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f'{self.email}{self.username}'


