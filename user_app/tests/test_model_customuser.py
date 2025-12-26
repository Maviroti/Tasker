import pytest
from user_app.models import CustomUser


@pytest.mark.django_db
class TestCustomUser:
    """Тесты для модели CustomUser"""

    def test_create_user(self):
        """Тест создания обычного пользователя"""
        user = CustomUser.objects.create_user(
            email="test@example.com",
            password="testpass123",
            full_name="Test User",
        )  # type: ignore

        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.check_password("testpass123")
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False
        assert str(user) == "Test User"

    def test_create_user_without_email(self):
        """Тест: создание пользователя без email должно вызвать ошибку"""
        with pytest.raises(ValueError, match="Users must have an email address"):
            CustomUser.objects.create_user(
                email="",
                password="testpass123",
                full_name="Test User",
            )  # type: ignore

    def test_create_superuser(self):
        """Тест создания суперпользователя"""
        superuser = CustomUser.objects.create_superuser(
            email="admin@example.com",
            password="adminpass123",
            full_name="Admin User",
        )  # type: ignore

        assert superuser.email == "admin@example.com"
        assert superuser.full_name == "Admin User"
        assert superuser.check_password("adminpass123")
        assert superuser.is_active is True
        assert superuser.is_staff is True
        assert superuser.is_superuser is True

    def test_email_uniqueness(self):
        """Тест уникальности email"""
        CustomUser.objects.create_user(
            email="unique@example.com",
            password="pass123",
            full_name="User One",
        )  # type: ignore

        # Попытка создать пользователя с таким же email должна вызвать ошибку
        with pytest.raises(Exception):  # django.db.utils.IntegrityError
            CustomUser.objects.create_user(
                email="unique@example.com",
                password="pass456",
                full_name="User Two",
            )  # type: ignore

    def test_update_user(self):
        """Тест обновления пользователя"""
        user = CustomUser.objects.create_user(
            email="  origin@example.com",
            password="originalpass",
            full_name="Original Name",
        )  # type: ignore

        # Обновление данных
        user.full_name = "Updated Name"
        user.email = "updated@example.com"
        user.save()

        # Проверка обновленных данных
        updated_user = CustomUser.objects.get(pk=user.pk)
        assert updated_user.full_name == "Updated Name"
        assert updated_user.email == "updated@example.com"

    def test_delete_user(self):
        """Тест удаления пользователя"""
        user = CustomUser.objects.create_user(
            email="delete@example.com",
            password="testpass",
            full_name="To Delete",
        )  # type: ignore

        user_id = user.id
        user.delete()

        # Проверка, что пользователь удален
        with pytest.raises(CustomUser.DoesNotExist):
            CustomUser.objects.get(pk=user_id)

    def test_user_normalize_email(self):
        """Тест нормализации email"""
        email = "TEST@EXAMPLE.COM"
        user = CustomUser.objects.create_user(
            email=email,
            password="testpass",
            full_name="Test User",
        )  # type: ignore

        assert user.email == "TEST@example.com"

    def test_username_is_optional(self):
        """Тест того, что username не обязателен"""
        user = CustomUser.objects.create_user(
            email="optional@example.com",
            password="testpass",
            full_name="Test User",
        )  # type: ignore

        assert user.username is None

    def test_user_required_fields(self):
        """Тест обязательных полей"""
        # Проверяем, что email - это USERNAME_FIELD
        assert CustomUser.USERNAME_FIELD == "email"

        # Проверяем, что REQUIRED_FIELDS пуст
        assert not CustomUser.REQUIRED_FIELDS

    def test_password_hashing(self):
        """Тест хеширования пароля"""
        user = CustomUser.objects.create_user(
            email="hash@example.com", password="plain_password", full_name="Test User"
        )  # type: ignore

        # Пароль должен быть захэширован
        assert user.password != "plain_password"

        # Проверка правильности пароля
        assert user.check_password("plain_password") is True
        assert user.check_password("wrong_password") is False


@pytest.mark.django_db
def test_multiple_users():
    """Тест создания нескольких пользователей"""
    users_data = [
        {"email": "user1@example.com", "full_name": "User One"},
        {"email": "user2@example.com", "full_name": "User Two"},
        {"email": "user3@example.com", "full_name": "User Three"},
    ]

    for data in users_data:
        CustomUser.objects.create_user(
            email=data["email"], password="commonpass", full_name=data["full_name"]
        )  # type: ignore

    assert CustomUser.objects.count() == 3
    emails = list(CustomUser.objects.values_list("email", flat=True))
    assert "user1@example.com" in emails
    assert "user2@example.com" in emails
    assert "user3@example.com" in emails
