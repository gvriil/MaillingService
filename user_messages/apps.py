from django.apps import AppConfig


class MessagesConfig(AppConfig):
    """Конфигурация приложения для пользовательских сообщений."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "user_messages"
