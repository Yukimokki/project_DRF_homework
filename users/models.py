from django.contrib.auth.models import AbstractUser
from django.db import models

from course_materials.models import Course, Lesson

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

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Cash"),
        ("transfer", "account transfer"),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="User",
        **NULLABLE,
    )
    payment_date = models.DateField(verbose_name="payment date")
    paid_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Paid course", **NULLABLE
    )
    separately_paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="A lesson paid separately",
        **NULLABLE,
    )
    payment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="total payment",
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name="Payment method",
    )

    payment_link = models.URLField(
        max_length=400,
        **NULLABLE,
        verbose_name="Link to the payment",
    )
    session_id = models.CharField(
        max_length=255,
        **NULLABLE,
        verbose_name="session ID",
    )


    def __str__(self):
        return f"{self.user} - {self.payment_amount} - {self.payment_date}"

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
