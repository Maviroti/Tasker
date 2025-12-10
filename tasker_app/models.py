from django.db import models
from datetime import date


class Task(models.Model):
    title = models.CharField(max_length=100)
    user_name = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    body = models.TextField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @classmethod
    def get_by_date(cls, target_date: date = date.today()):
        """Получить задачи по конкретной дате"""
        return Task.objects.filter(end_date=target_date)


class User(models.Model):
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.full_name}"
