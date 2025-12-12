from datetime import date
from django.contrib import admin
from .models import User, Task, Tag


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("full_name",)
    ordering = ("full_name",)
    list_filter = ("full_name",)
    search_fields = ("full_name",)
    search_help_text = "Поиск по имени пользователя"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "user_name", "end_date", "created_at")
    ordering = ("end_date", "title")
    list_filter = ("user_name", "end_date", "created_at")
    search_fields = ("title", "user_name__full_name", "body", "end_date", "created_at")
    search_help_text = "Поиск по всем полям задачи"

    @admin.action(description='Сделать дату окончания "Сегодня"')
    def set_end_date_today(self, request, queryset):
        for task in queryset:
            task.end_date = date.today()
            task.save()

    actions = (set_end_date_today,)  # type: ignore


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    search_help_text = "Поиск по имени тега"
