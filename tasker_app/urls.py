from django.urls import path
from .views import (
    TaskDeleteView,
    TaskDetailView,
    TaskUpdateView,
    IndexTemplateView,
    KanbanTemplateView,
    AboutTemplateView,
    TodayTemplateView,
    TaskCreateView,
)

urlpatterns = [
    path("", IndexTemplateView.as_view(), name="index"),
    path("kanban/", KanbanTemplateView.as_view(), name="kanban"),
    path("about/", AboutTemplateView.as_view(), name="about"),
    path("today/", TodayTemplateView.as_view(), name="today"),
    path("tasks/add/", TaskCreateView.as_view(), name="add_task_form"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("tasks/<int:pk>/edit/", TaskUpdateView.as_view(), name="task_edit"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
]
