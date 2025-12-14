from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    """Форма для создания пользователя"""

    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите Email"}
        ),
    )

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"}
        ),
        help_text="",
    )

    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Подтвердите пароль"}
        ),
        help_text="",
    )

    class Meta:
        model = get_user_model()
        fields = ["email", "full_name"]
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже занят")
        return email


class CustomAuthenticationForm(AuthenticationForm):
    """Форма для аутентификации пользователя"""

    username = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите Email"}
        ),
    )

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"}
        ),
    )

    def clean_username(self):
        username = self.cleaned_data.get("username").lower()
        return username
