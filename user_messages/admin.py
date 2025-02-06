from django.contrib import admin
from .models import UserMessage


@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    """Административный интерфейс для управления пользовательскими сообщениями."""

    list_display = ("owner", "subject", "body")  # Настройте по мере необходимости
