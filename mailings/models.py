from config.settings import NULLABLE
from django.conf import settings
from django.db import models


class Mailing(models.Model):
    """Модель для представления рассылки."""

    FREQ_CHOICES = [
        ("daily", "ежедневно"),
        ("weekly", "раз в неделю"),
        ("monthly", "раз в месяц"),
        ("yearly", "раз в год"),
    ]

    STATUS_CHOICES = [
        ("created", "создана"),
        ("running", "в работе"),
        ("completed", "выполнена"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="User",
    )
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_datetime = models.DateTimeField(verbose_name="Start Date and Time")
    end_datetime = models.DateTimeField(verbose_name="End Date and Time", **NULLABLE)
    frequency = models.CharField(
        max_length=250, verbose_name="Frequency", choices=FREQ_CHOICES, default="weekly"
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="created")
    message = models.ForeignKey(
        "user_messages.UserMessage", on_delete=models.SET_NULL, **NULLABLE
    )
    clients = models.ManyToManyField("clients.Client")

    class Meta:
        ordering = ["-start_datetime"]

    def __str__(self):
        """Возвращает строковое представление рассылки."""
        return f"Mailing {self.start_datetime} [{self.status}]"


class Message(models.Model):
    """Модель для представления сообщения."""

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE
    )
    subject = models.CharField(max_length=255, verbose_name="Subject")
    body = models.TextField(verbose_name="Body")

    def __str__(self):
        """Возвращает строковое представление сообщения."""
        return self.subject


class Attempt(models.Model):
    """Модель для представления попытки отправки рассылки."""

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, **NULLABLE)
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, verbose_name="Status")
    server_response = models.TextField(**NULLABLE)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE
    )

    def __str__(self):
        """Возвращает строковое представление попытки."""
        return f"Attempt {self.date_time} [{self.status}]"
