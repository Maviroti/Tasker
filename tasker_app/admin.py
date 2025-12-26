from datetime import date
from django.contrib import admin
from .models import Task, Tag


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Админка для задачи"""

    list_display = ("title", "user_name", "end_date", "created_at")
    ordering = ("end_date", "title")
    list_filter = ("user_name", "end_date", "created_at")
    search_fields = ("title", "user_name__full_name", "body", "end_date", "created_at")
    search_help_text = "Поиск по всем полям задачи"

    @admin.action(description='Сделать дату окончания "Сегодня"')
    def set_end_date_today(self, request, queryset):
        """Сделать дату окончания "Сегодня" для выбранных задач"""
        for task in queryset:
            task.end_date = date.today()
            task.save()

    actions = (set_end_date_today,)  # type: ignore


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админка для тега"""

    list_display = ("name",)
    ordering = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    search_help_text = "Поиск по имени тега"
