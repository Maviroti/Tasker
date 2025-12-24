from celery import shared_task


@shared_task
def log_new_task(task_name: str) -> str:
    """Выводит в консоль сообщение о создании задачи"""
    msg = f"Создана новая задача: {task_name}"
    print(msg)  # Вывод сообщения в консоль воркера
    return msg  # Возвращаем сообщение для вывода в консоль сервера
