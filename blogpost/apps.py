from django.apps import AppConfig


class BlogpostConfig(AppConfig):
    """Конфигурация приложения для блога."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "blogpost"
