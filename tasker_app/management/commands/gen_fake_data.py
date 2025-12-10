from django.core.management.base import BaseCommand
from faker import Faker
from tasker_app.models import Task, User
import random


class Command(BaseCommand):
    help = "Генерация данных"

    def handle(self, *args, **kwargs):
        self.stdout.write("Начинаем генерацию данных...")

        fake = Faker()

        users = []
        for i in range(random.randint(3, 5)):
            user = User.objects.create(
                full_name=fake.name(),
            )
            users.append(user)
        self.stdout.write(f"Создали {len(users)} пользователей")

        tasks = []
        for i in range(random.randint(5, 10)):
            task_title = fake.sentence(nb_words=6)
            task_user = random.choice(users)
            task_body = fake.text(max_nb_chars=200)

            task = Task.objects.create(
                title=task_title,
                body=task_body,
                user_name=task_user,
                end_date=fake.date_this_year(),
            )
            tasks.append(task)
        self.stdout.write(f"Создали {len(tasks)} задач")

        self.stdout.write("Генерация данных завершена")
