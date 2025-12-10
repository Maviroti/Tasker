from django.urls import path
from .views import (
    TaskDeleteView,
    TaskDetailView,
    TaskUpdateView,
    index,
    about,
    today,
    TaskCreateView,
)

urlpatterns = [
    path("", index, name="index"),
    path("about/", about, name="about"),
    path("today/", today, name="today"),
    path("tasks/add/", TaskCreateView.as_view(), name="add_task_form"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("tasks/<int:pk>/edit/", TaskUpdateView.as_view(), name="task_edit"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
]
