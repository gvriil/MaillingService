from django.urls import path
from .views import (
    MessageListView,
    MessageDetailView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView,
)

app_name = "user_messages"

urlpatterns = [
    path("", MessageListView.as_view(), name="list"),  # Список сообщений
    path("<int:pk>/", MessageDetailView.as_view(), name="detail"),  # Детали сообщения
    path(
        "create/", MessageCreateView.as_view(), name="create"
    ),  # Создание нового сообщения
    path(
        "update/<int:pk>/", MessageUpdateView.as_view(), name="update"
    ),  # Обновление сообщения
    path(
        "delete/<int:pk>/", MessageDeleteView.as_view(), name="delete"
    ),  # Удаление сообщения
]
