from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.contrib import messages

from tasker_app.forms import TaskModelForm
from tasker_app.models import Task
from tasker_app.tasks import log_new_task


class IndexTemplateView(TemplateView):
    """Представление главной страницы"""

    template_name = "tasker_app/index.html"

    def get_context_data(self, **kwargs):
        tasks = Task.objects.all()
        context = super().get_context_data(**kwargs)
        context["active_page"] = "index"
        context["tasks"] = tasks
        return context


class KanbanTemplateView(TemplateView):
    """Представление для канбана"""

    template_name = "tasker_app/kanban.html"

    def get_context_data(self, **kwargs):
        new_tasks = Task.objects.filter(status=Task.TaskStatus.NEW)
        active_tasks = Task.objects.filter(status=Task.TaskStatus.ACTIVE)
        closed_tasks = Task.objects.filter(status=Task.TaskStatus.CLOSED)
        context = super().get_context_data(**kwargs)
        context["active_page"] = "index"
        context["new_tasks"] = new_tasks
        context["active_tasks"] = active_tasks
        context["closed_tasks"] = closed_tasks
        return context


class AboutTemplateView(TemplateView):
    """Представление страницы about"""

    template_name = "tasker_app/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_page"] = "about"
        return context


class TodayTemplateView(TemplateView):
    """Представление страницы today"""

    template_name = "tasker_app/index.html"

    def get_context_data(self, **kwargs):
        today_tasks = Task.get_by_date()
        context = super().get_context_data(**kwargs)
        context["active_page"] = "today"
        context["tasks"] = today_tasks
        return context


class TaskCreateView(CreateView):
    """Представление для формы создания задачи"""

    model = Task
    template_name = "tasker_app/task_add.html"
    form_class = TaskModelForm

    def get_success_url(self):
        return reverse_lazy("task_detail", kwargs={"pk": self.object.pk})  # type: ignore

    def form_valid(self, form):
        """Добавляем сообщение об успешном создании задачи."""
        response = super().form_valid(form)
        messages.success(self.request, "Пост успешно создан")

        # логируем в консоль результат задачи celery
        task_result = log_new_task.delay(str(self.object.title))  # type: ignore
        print(task_result.get())
        return response


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

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_staff:
            return super().delete(request, *args, **kwargs)
        messages.error(self.request, "У вас нет прав на удаление задачи")
        return reverse_lazy("index")
