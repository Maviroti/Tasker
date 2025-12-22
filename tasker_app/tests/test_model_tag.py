import pytest

from tasker_app.models import Tag


@pytest.mark.django_db
class TestTagModel:
    """Тесты для модели Tag"""

    def test_create_tag(self):
        """Тест создания тега"""
        tag = Tag.objects.create(name="Важный")

        assert tag.name == "Важный"
        assert str(tag) == "Важный"
        assert tag.id is not None

    def test_create_multiple_tags(self):
        """Тест создания нескольких тегов"""
        tags_data = ["Срочный", "База данных", "Фронтенд", "Бэкенд"]

        for tag_name in tags_data:
            Tag.objects.create(name=tag_name)

        assert Tag.objects.count() == 4
        tag_names = list(Tag.objects.values_list("name", flat=True))
        for tag_name in tags_data:
            assert tag_name in tag_names

    def test_tag_str_representation(self):
        """Тест строкового представления тега"""
        tag = Tag.objects.create(name="Тестовый тег")

        assert str(tag) == "Тестовый тег"

    def test_update_tag(self):
        """Тест обновления тега"""
        tag = Tag.objects.create(name="Старое название")
        tag.name = "Новое название"
        tag.save()

        updated_tag = Tag.objects.get(pk=tag.pk)
        assert updated_tag.name == "Новое название"

    def test_delete_tag(self):
        """Тест удаления тега"""
        tag = Tag.objects.create(name="Удаляемый тег")
        tag_id = tag.id
        tag.delete()

        with pytest.raises(Tag.DoesNotExist):
            Tag.objects.get(pk=tag_id)
