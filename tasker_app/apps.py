from django.apps import AppConfig


class TaskerAppConfig(AppConfig):
    """Класс для конфигурации приложения"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "tasker_app"
