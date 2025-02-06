from blogpost.forms import StyleFormMixin
from django import forms
from mailings.models import Mailing
from clients.models import Client
from user_messages.models import UserMessage as Message


class MailingForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания и редактирования рассылки."""

    class Meta:
        model = Mailing
        fields = ["start_datetime", "end_datetime", "frequency", "message", "clients"]

        exclude = ("owner", "status")

        widgets = {
            "start_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_datetime": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        """Инициализация формы с фильтрацией сообщений и клиентов по владельцу."""
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["message"].queryset = Message.objects.filter(owner=user)
        self.fields["clients"].queryset = Client.objects.filter(owner=user)


class MessageForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания и редактирования сообщения."""

    class Meta:
        model = Message
        fields = "__all__"


class MailingModeratorForm(StyleFormMixin, forms.ModelForm):
    """Форма для модерации статуса рассылки."""

    class Meta:
        model = Mailing
        fields = ("status",)
