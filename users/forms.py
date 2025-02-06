from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)

from users.models import User


class StyleFormMixin:
    """
    Миксин для добавления стилей к полям формы.

    Методы:
        __init__: Добавляет классы CSS к полям формы.
    """

    def __init__(self, *args, **kwargs):
        """
        Инициализация миксина. Добавляет классы CSS к полям формы.

        :param args: Позиционные аргументы.
        :param kwargs: Именованные аргументы.
        """
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    """
    Форма для входа пользователя.

    Методы:
        __init__: Добавляет стили к полям формы.
    """

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы. Добавляет классы CSS к полям формы.

        :param args: Позиционные аргументы.
        :param kwargs: Именованные аргументы.
        """
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """
    Форма для регистрации нового пользователя.

    Атрибуты:
        Meta: Метаданные формы, включая модель и поля.
    """

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class UserForm(StyleFormMixin, UserChangeForm):
    """
    Форма для редактирования данных пользователя.
    """

    new_password = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False,
    )

    class Meta:
        model = User
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.HiddenInput()

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("new_password")
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user


class PasswordResetRequestForm(StyleFormMixin, forms.Form):
    """
    Форма для запроса сброса пароля.

    Атрибуты:
        email (EmailField): Поле для ввода email пользователя.
    """

    email = forms.EmailField(
        label="Введите ваш email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
