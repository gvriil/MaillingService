from mailings.models import NULLABLE
from django.conf import settings
from django.db import models


class UserMessage(models.Model):
    """Модель для хранения сообщений пользователей."""

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE
    )
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        """Возвращает строковое представление сообщения (тему)."""
        return self.subject
