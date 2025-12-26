from django import forms
from django.core.exceptions import ValidationError
from tasker_app.models import Task


class TaskModelForm(forms.ModelForm):
    """Форма для модели Task"""

    class Meta:
        """Класс для настройки формы"""

        model = Task
        fields = [
            "task_type",
            "status",
            "title",
            "user_name",
            "body",
            "tags",
            "end_date",
        ]
        labels = {
            "task_type": "Тип",
            "status": "Статус",
            "title": "Название",
            "user_name": "Пользователь",
            "body": "Содержание",
            "tags": "Теги",
            "end_date": "Дата окончания задачи",
        }
        widgets = {
            "task_type": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите название задачи",
                }
            ),
            "user_name": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "body": forms.Textarea(
                attrs={
                    "class": "form-control my-textarea",
                    "rows": 4,
                    "placeholder": "Введите содержание задачи",
                }
            ),
            "tags": forms.SelectMultiple(
                attrs={
                    "class": "form-control",
                }
            ),
            "end_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # При создании новой задачи
        if not self.instance.pk:
            # Добавляем атрибут disabled к виджету
            self.fields["status"].widget.attrs["disabled"] = True

    def clean_title(self):
        """Валидация title на количество слов"""
        title: str = str(self.cleaned_data.get("title"))
        words_list = title.split()
        if len(words_list) < 2:
            raise ValidationError("Название должно содержать минимум 2 слова")
        return title
