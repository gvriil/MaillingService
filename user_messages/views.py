from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.core.exceptions import PermissionDenied
from .models import UserMessage


class MessageListView(ListView):
    """Представление для отображения списка сообщений пользователя."""

    model = UserMessage
    template_name = "user_messages/message_list.html"

    def get_queryset(self):
        """Возвращает сообщения, принадлежащие текущему пользователю."""
        return UserMessage.objects.filter(owner=self.request.user)


class MessageDetailView(DetailView):
    """Представление для отображения деталей сообщения."""

    model = UserMessage
    template_name = "user_messages/message_detail.html"


class MessageCreateView(CreateView):
    """Представление для создания нового сообщения."""

    model = UserMessage
    fields = ["subject", "body"]  # Убрал поле 'user'
    template_name = "user_messages/message_form.html"
    success_url = reverse_lazy("user_messages:list")

    def form_valid(self, form):
        """Устанавливает текущего пользователя как владельца сообщения перед сохранением."""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    """Представление для редактирования существующего сообщения."""

    model = UserMessage
    fields = ["subject", "body"]  # Убрал поле 'user'
    template_name = "user_messages/message_form.html"

    def get_success_url(self):
        """Возвращает URL для перенаправления после успешного обновления сообщения."""
        return reverse_lazy("user_messages:detail", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        """Получает объект сообщения и проверяет права доступа пользователя."""
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise PermissionDenied("У вас нет прав для редактирования этого сообщения.")
        return obj


class MessageDeleteView(DeleteView):
    """Представление для удаления сообщения."""

    model = UserMessage
    success_url = reverse_lazy("user_messages:list")
    template_name = "user_messages/message_confirm_delete.html"

    def get_object(self, queryset=None):
        """Получает объект сообщения и проверяет права доступа пользователя."""
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise PermissionDenied("У вас нет прав для удаления этого сообщения.")
        return obj
