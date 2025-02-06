from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import TemplateView

from users.apps import UsersConfig
from .views import (
    CustomLoginView,
    RegisterView,
    UserUpdateView,
    PasswordResetView,
    UserDeleteView,
)

app_name = UsersConfig.name

urlpatterns = [
    path(
        "login/",
        CustomLoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path("logout/", LogoutView.as_view(next_page="users:login"), name="logout"),
    path(
        "profile/",
        TemplateView.as_view(template_name="users/profile.html"),
        name="profile",
    ),
    path("register/", RegisterView.as_view(), name="register"),
    path("accounts/profile/", UserUpdateView.as_view(), name="user_edit"),
    # Password reset URL
    path(
        "password_reset/",
        PasswordResetView.as_view(),
        name="password_reset",
    ),
    # Optional: A done view to inform the user that the password reset email has been sent
    path(
        "password_reset_done/",
        TemplateView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path("accounts/delete/", UserDeleteView.as_view(), name="user_delete"),
]

# Докстринги для модуля
"""
Модуль `urls` приложения `users` определяет маршруты (URL-адреса) для работы с пользователями.

Маршруты включают:
- Вход (login) и выход (logout) пользователя.
- Регистрацию нового пользователя.
- Просмотр и редактирование профиля пользователя.
- Сброс пароля и завершение сброса пароля.

Каждый маршрут связан с соответствующим представлением (view), которое обрабатывает запросы
и возвращает ответы пользователю.
"""
