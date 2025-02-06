import random
import string

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from users.forms import (
    UserRegisterForm,
    UserLoginForm,
    PasswordResetRequestForm,
    UserForm,
)
from users.models import User


@login_required
def profile(request):
    """
    Отображение профиля пользователя.

    Args:
        request: Запрос от пользователя.

    Returns:
        Рендер страницы профиля с данными текущего пользователя.
    """
    return render(request, "users/profile.html", {"user": request.user})


class CustomLoginView(LoginView):
    """
    Кастомное представление для входа пользователя.

    Использует форму UserLoginForm и шаблон users/login.html.
    """

    form_class = UserLoginForm
    template_name = "users/login.html"

    def dispatch(self, request, *args, **kwargs):
        """Проверяет, аутентифицирован ли пользователь, и перенаправляет на домашнюю страницу, если да."""
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)


class RegisterView(CreateView):
    """
    Представление для регистрации нового пользователя.

    Использует форму UserRegisterForm и шаблон users/register.html.
    После успешной регистрации отправляет письмо на email пользователя.
    """

    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        """
        Обработка успешной регистрации.

        Args:
            form: Валидная форма регистрации.

        Returns:
            Редирект на страницу входа после успешной регистрации.
        """
        new_user = form.save()
        try:
            send_mail(
                subject="Поздравляем, вы зарегистрированы!",
                message="Вы успешно зарегистрированы на нашем сайте.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[new_user.email],
                fail_silently=False,
            )
            messages.success(
                self.request, "Письмо с подтверждением отправлено на ваш email."
            )
        except Exception as e:
            messages.error(
                self.request,
                "Не удалось отправить письмо. Пожалуйста, попробуйте позже.",
            )
            print(f"Ошибка отправки email: {e}")
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    """
    Представление для редактирования профиля пользователя.
    """

    model = User
    form_class = UserForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Ваш профиль был успешно обновлен.")
        return super().form_valid(form)


def forgot_password(request):
    """
    Заглушка для сброса пароля.

    Args:
        request: Запрос от пользователя.

    Returns:
        Редирект на страницу входа.
    """
    request.user.set_password()
    request.user.save()
    return redirect(reverse("users:login"))


class PasswordResetView(View):
    form_class = PasswordResetRequestForm
    template_name = "users/password_reset_form.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.filter(email=email).first()
            if user:
                new_password = "".join(
                    random.choices(string.ascii_letters + string.digits, k=20)
                )
                user.set_password(new_password)
                user.save()
                send_mail(
                    "Восстановление пароля",
                    f"Ваш новый пароль: {new_password}",
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, "Новый пароль отправлен на ваш email.")
                return redirect("users:login")
            else:
                messages.error(request, "Пользователь с таким email не найден.")
        return render(request, self.template_name, {"form": form})


class UserDeleteView(DeleteView):
    """
    Представление для удаления аккаунта пользователя.
    """

    model = User
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("users:login")

    def get_object(self, queryset=None):
        """
        Получение объекта пользователя для удаления.

        Returns:
            Текущий авторизованный пользователь.
        """
        return self.request.user

    def post(self, request, *args, **kwargs):
        """
        Обработка POST-запроса для удаления пользователя.
        """
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, "Ваш аккаунт был успешно удален.")
        return redirect(self.success_url)
