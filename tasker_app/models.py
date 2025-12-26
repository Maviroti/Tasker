from datetime import date
from django.db import models

from user_app.models import CustomUser


class Task(models.Model):
    """Модель задачи"""

    class TaskType(models.TextChoices):
        """Типы задач"""

        TASK = "task", "Task"
        BUG = "bug", "Bug"
        FEATURE = "feature", "Feature"
        PBI = "pbi", "Product Backlog Item"
        EPIC = "epic", "Epic"

    class TaskStatus(models.TextChoices):
        """Статусы задач"""

        ACTIVE = "active", "Active"
        CLOSED = "closed", "Closed"
        NEW = "new", "New"

    title = models.CharField(max_length=100)
    user_name = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    body = models.TextField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField("Tag", related_name="tasks", blank=True)
    task_type = models.CharField(
        max_length=20,
        choices=TaskType.choices,
        default=TaskType.TASK,
        verbose_name="Тип задачи",
    )
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.NEW,
        verbose_name="Статус задачи",
        blank=True,
    )

    def __str__(self):
        return str(self.title)

    @classmethod
    def get_by_date(cls, target_date: date = date.today()):
        """Получить задачи по конкретной дате"""
        return Task.objects.filter(end_date=target_date)

    def get_tags_list(self) -> list:
        """Получить список тегов задачи"""
        return [tag.name for tag in self.tags.all()]

    def get_str_with_all_tags(self) -> str:
        """Получить строку с тегами задачи"""
        return ", ".join(self.get_tags_list())


class Tag(models.Model):
    """Модель тегов для задач"""

    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)
