from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from tasker_app.forms import TaskModelForm
from tasker_app.models import Task


def index(request):
    """Главная страница"""
    tasks = Task.objects.all()
    context = {
        "active_page": "index",
        "tasks": tasks,
    }
    return render(request, "tasker_app/index.html", context=context)


def about(request):
    """Выводим страницу about"""
    context = {
        "active_page": "about",
    }
    return render(request, "tasker_app/about.html", context=context)


def today(request):
    """Выводим список задач у которых сегодня последний день"""
    today_tasks = Task.get_by_date()
    context = {
        "active_page": "today",
        "tasks": today_tasks,
    }
    return render(request, "tasker_app/index.html", context=context)


class TaskCreateView(CreateView):
    """Представление для формы создания задачи"""

    model = Task
    template_name = "tasker_app/task_add.html"
    form_class = TaskModelForm

    def get_success_url(self):
        return reverse_lazy("task_detail", kwargs={"pk": self.object.pk})  # type: ignore


class TaskDetailView(DetailView):
    """Представление для детального просмотра задачи"""

    model = Task
    template_name = "tasker_app/task_detail.html"


class TaskUpdateView(UpdateView):
    """Представление для формы изменения задачи"""

    model = Task
    template_name = "tasker_app/task_edit.html"
    form_class = TaskModelForm

    def get_success_url(self):
        return reverse_lazy("task_detail", kwargs={"pk": self.get_object().pk})


class TaskDeleteView(DeleteView):
    """Представление для удаления задачи"""

    model = Task

    def get_success_url(self):
        return reverse_lazy("index")
