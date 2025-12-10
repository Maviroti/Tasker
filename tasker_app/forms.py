from django import forms
from tasker_app.models import Task


class TaskModelForm(forms.ModelForm):
    """Форма для модели Task"""

    class Meta:
        model = Task
        fields = [
            "title",
            "user_name",
            "body",
            "end_date",
        ]
        labels = {
            "title": "Название",
            "user_name": "Пользователь",
            "body": "Содержание",
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
                    "placeholder": "Введите имя пользователя",
                }
            ),
            "body": forms.Textarea(
                attrs={
                    "class": "form-control my-textarea",
                    "rows": 4,
                    "placeholder": "Введите содержание задачи",
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
        # Добавляем data-original атрибут ко всем полям
        for field_name, field in self.fields.items():
            # Добавляем data-original только если есть значение
            if self.instance and self.instance.pk:
                value = getattr(self.instance, field_name)
                if field_name == "end_date" and value:
                    field.widget.attrs["data-original"] = value.strftime("%Y-%m-%d")
                elif value:
                    field.widget.attrs["data-original"] = str(value)
