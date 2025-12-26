from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    """Модель менеджера пользователей"""

    def create_user(self, email, password=None, **extra_fields):
        """Создание пользователя"""
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Создание администратора"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """Модель кастомного пользователя"""

    full_name = models.CharField(max_length=100, verbose_name="Имя пользователя")
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    username = models.CharField(
        max_length=100,
        unique=False,
        blank=True,
        null=True,
        verbose_name="Имя пользователя (не обязательное)",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.full_name}"
