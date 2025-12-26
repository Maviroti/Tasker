from datetime import date, timedelta
import pytest

from tasker_app.models import Task, Tag
from user_app.models import CustomUser


@pytest.mark.django_db
class TestTaskModel:
    """Тесты для модели Task"""

    @pytest.fixture
    def test_user(self):
        """Фикстура для создания тестового пользователя"""
        return CustomUser.objects.create_user(
            email="testuser@example.com", password="testpass123", full_name="Test User"
        )  # type: ignore

    @pytest.fixture
    def test_tags(self):
        """Фикстура для создания тестовых тегов"""
        tags = []
        tag_names = ["Важный", "Срочный", "Баг"]
        for name in tag_names:
            tags.append(Tag.objects.create(name=name))
        return tags

    def test_create_task_with_required_fields(self, test_user):
        """Тест создания задачи с обязательными полями"""
        tomorrow = date.today() + timedelta(days=1)
        task = Task.objects.create(
            title="Тестовая задача",
            user_name=test_user,
            body="Описание тестовой задачи",
            end_date=tomorrow,
        )

        assert task.title == "Тестовая задача"
        assert task.user_name == test_user
        assert task.body == "Описание тестовой задачи"
        assert task.end_date == tomorrow
        assert task.task_type == "task"  # Значение по умолчанию
        assert task.status == "new"  # Значение по умолчанию
        assert task.created_at is not None
        assert str(task) == "Тестовая задача"

    def test_create_task_with_all_fields(self, test_user, test_tags):
        """Тест создания задачи со всеми полями"""
        tomorrow = date.today() + timedelta(days=1)
        task = Task.objects.create(
            title="Создание новой фичи",
            user_name=test_user,
            body="Добавить авторизацию по OAuth2",
            end_date=tomorrow,
            task_type="feature",
            status="active",
        )

        # Добавляем теги к задаче
        task.tags.set(test_tags)

        assert task.title == "Создание новой фичи"
        assert task.task_type == "feature"
        assert task.status == "active"
        assert task.tags.count() == 3
        assert list(task.tags.all()) == test_tags

    def test_task_type_choices(self):
        """Тест доступных типов задач"""
        task_types = dict(Task.TaskType.choices)

        assert len(task_types) == 5
        assert "task" in task_types
        assert "bug" in task_types
        assert "feature" in task_types
        assert "pbi" in task_types
        assert "epic" in task_types
        assert task_types["task"] == "Task"
        assert task_types["bug"] == "Bug"
        assert task_types["feature"] == "Feature"
        assert task_types["pbi"] == "Product Backlog Item"
        assert task_types["epic"] == "Epic"

    def test_task_status_choices(self):
        """Тест доступных статусов задач"""
        task_statuses = dict(Task.TaskStatus.choices)

        assert len(task_statuses) == 3
        assert "active" in task_statuses
        assert "closed" in task_statuses
        assert "new" in task_statuses
        assert task_statuses["active"] == "Active"
        assert task_statuses["closed"] == "Closed"
        assert task_statuses["new"] == "New"

    def test_get_by_date_method(self, test_user):
        """Тест метода get_by_date"""
        today = date.today()
        tomorrow = today + timedelta(days=1)

        # Создаем задачи на разные даты
        task_today = Task.objects.create(
            title="Задача на сегодня",
            user_name=test_user,
            body="Описание",
            end_date=today,
        )

        task_tomorrow = Task.objects.create(
            title="Задача на завтра",
            user_name=test_user,
            body="Описание",
            end_date=tomorrow,
        )

        task_today2 = Task.objects.create(
            title="Еще задача на сегодня",
            user_name=test_user,
            body="Описание",
            end_date=today,
        )

        # Получаем задачи на сегодня
        today_tasks = Task.get_by_date(today)
        assert today_tasks.count() == 2
        assert task_today in today_tasks
        assert task_today2 in today_tasks
        assert task_tomorrow not in today_tasks

        # Получаем задачи на завтра
        tomorrow_tasks = Task.get_by_date(tomorrow)
        assert tomorrow_tasks.count() == 1
        assert task_tomorrow in tomorrow_tasks

        # Проверяем значение по умолчанию (сегодня)
        default_tasks = Task.get_by_date()
        assert default_tasks.count() == 2

    def test_get_tags_list_method(self, test_user, test_tags):
        """Тест метода get_tags_list"""
        task = Task.objects.create(
            title="Задача с тегами",
            user_name=test_user,
            body="Описание",
            end_date=date.today(),
        )

        task.tags.set(test_tags)

        tags_list = task.get_tags_list()
        assert isinstance(tags_list, list)
        assert len(tags_list) == 3
        assert "Важный" in tags_list
        assert "Срочный" in tags_list
        assert "Баг" in tags_list

    def test_get_str_with_all_tags_method(self, test_user, test_tags):
        """Тест метода get_str_with_all_tags"""
        task = Task.objects.create(
            title="Задача с тегами",
            user_name=test_user,
            body="Описание",
            end_date=date.today(),
        )

        task.tags.set(test_tags)

        tags_str = task.get_str_with_all_tags()
        assert isinstance(tags_str, str)
        # Порядок может быть разным, поэтому проверяем наличие всех тегов
        assert "Важный" in tags_str
        assert "Срочный" in tags_str
        assert "Баг" in tags_str
        assert tags_str.count(",") == 2  # Два разделителя для трех тегов

    def test_task_without_tags(self, test_user):
        """Тест задачи без тегов"""
        task = Task.objects.create(
            title="Задача без тегов",
            user_name=test_user,
            body="Описание",
            end_date=date.today(),
        )

        assert task.tags.count() == 0
        assert task.get_tags_list() == []
        assert task.get_str_with_all_tags() == ""

    def test_update_task(self, test_user):
        """Тест обновления задачи"""
        task = Task.objects.create(
            title="Старый заголовок",
            user_name=test_user,
            body="Старое описание",
            end_date=date.today(),
            status="new",
        )

        # Обновление данных
        new_date = date.today() + timedelta(days=7)
        task.title = "Новый заголовок"
        task.body = "Новое описание"
        task.end_date = new_date
        task.status = "active"
        task.task_type = "bug"
        task.save()

        updated_task = Task.objects.get(pk=task.pk)
        assert updated_task.title == "Новый заголовок"
        assert updated_task.body == "Новое описание"
        assert updated_task.end_date == new_date
        assert updated_task.status == "active"
        assert updated_task.task_type == "bug"

    def test_delete_task(self, test_user):
        """Тест удаления задачи"""
        task = Task.objects.create(
            title="Удаляемая задача",
            user_name=test_user,
            body="Описание",
            end_date=date.today(),
        )

        task_id = task.id
        task.delete()

        with pytest.raises(Task.DoesNotExist):
            Task.objects.get(pk=task_id)

    def test_task_foreign_key_relationship(self, test_user):
        """Тест связи ForeignKey с пользователем"""
        # Создаем несколько задач для одного пользователя
        for i in range(3):
            Task.objects.create(
                title=f"Задача {i}",
                user_name=test_user,
                body=f"Описание {i}",
                end_date=date.today() + timedelta(days=i),
            )

        # Проверяем связь
        assert test_user.tasks.count() == 3

        # Проверяем удаление пользователя (каскадное удаление)
        user_id = test_user.id
        test_user.delete()

        # Задачи должны быть удалены
        assert Task.objects.filter(user_name_id=user_id).count() == 0

    def test_task_many_to_many_relationship(self, test_user, test_tags):
        """Тест связи ManyToMany с тегами"""
        task = Task.objects.create(
            title="Задача с тегами",
            user_name=test_user,
            body="Описание",
            end_date=date.today(),
        )

        # Добавляем теги
        task.tags.add(test_tags[0], test_tags[1])

        assert task.tags.count() == 2
        assert test_tags[0] in task.tags.all()
        assert test_tags[1] in task.tags.all()
        assert test_tags[2] not in task.tags.all()

        # Удаляем один тег
        task.tags.remove(test_tags[0])
        assert task.tags.count() == 1
        assert test_tags[0] not in task.tags.all()
        assert test_tags[1] in task.tags.all()

        # Очищаем все теги
        task.tags.clear()
        assert task.tags.count() == 0

    def test_task_with_custom_status(self, test_user):
        """Тест задачи со статусом не по умолчанию"""
        task = Task.objects.create(
            title="Закрытая задача",
            user_name=test_user,
            body="Описание",
            end_date=date.today(),
            status="closed",
        )

        assert task.status == "closed"
        assert task.get_status_display() == "Closed"


@pytest.mark.django_db
def test_task_tag_through_relationship():
    """Тест сквозной связи задачи и тегов"""
    user = CustomUser.objects.create_user(
        email="relation@example.com", password="testpass", full_name="Relation User"
    )  # type: ignore

    # Создаем теги
    tag1 = Tag.objects.create(name="Бэкенд")
    tag2 = Tag.objects.create(name="Фронтенд")
    tag3 = Tag.objects.create(name="Тестирование")

    # Создаем задачу с тегами
    task = Task.objects.create(
        title="Разработка фичи",
        user_name=user,
        body="Описание",
        end_date=date.today(),
    )

    task.tags.add(tag1, tag2, tag3)

    # Проверяем с обеих сторон
    assert task.tags.count() == 3
    assert tag1.tasks.count() == 1
    assert tag2.tasks.count() == 1
    assert tag3.tasks.count() == 1
    assert task in tag1.tasks.all()
    assert task in tag2.tasks.all()
    assert task in tag3.tasks.all()
