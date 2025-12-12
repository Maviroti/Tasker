from django import forms
from tasker_app.models import Task
from django.core.exceptions import ValidationError


class TaskModelForm(forms.ModelForm):
    """Форма для модели Task"""

    class Meta:
        model = Task
        fields = [
            "title",
            "user_name",
            "body",
            "tags",
            "end_date",
        ]
        labels = {
            "title": "Название",
            "user_name": "Пользователь",
            "body": "Содержание",
            "tags": "Теги",
            "end_date": "Дата окончания задачи",
        }
        widgets = {
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

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Добавляем data-original атрибут ко всем полям
    #     for field_name, field in self.fields.items():
    #         # Добавляем data-original только если есть значение
    #         if self.instance and self.instance.pk:
    #             value = getattr(self.instance, field_name)
    #             if field_name == "end_date" and value:
    #                 field.widget.attrs["data-original"] = value.strftime("%Y-%m-%d")
    #             elif value:
    #                 field.widget.attrs["data-original"] = str(value)

    def clean_title(self):
        """Валидация title на количество слов"""
        title: str = str(self.cleaned_data.get("title"))
        words_list = title.split()
        print(f"validation: {words_list}")
        if len(words_list) < 2:
            raise ValidationError("Название должно содержать минимум 2 слова")
        return title
