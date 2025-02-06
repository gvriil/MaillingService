from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import NULLABLE


class User(AbstractUser):
    """
    Модель пользователя, расширяющая стандартную модель AbstractUser.

    Атрибуты:
        username (CharField): Уникальное имя пользователя.
        email (EmailField): Уникальный адрес электронной почты.
        name (CharField): Фамилия, имя и отчество пользователя (необязательное поле).
        comment (CharField): Комментарий или дополнительная информация о пользователе (необязательное поле).
        avatar (ImageField): Аватар пользователя (необязательное поле).
        phone (CharField): Номер телефона пользователя (необязательное поле).
        country (CharField): Страна пользователя (необязательное поле).

    Методы:
        __str__: Возвращает строковое представление пользователя (email).
    """

    username = models.CharField(
        max_length=100,
        verbose_name="Пользователь",
        unique=True,
    )
    email = models.EmailField(
        max_length=100,
        verbose_name="Контактная эл. почта",
        unique=True,
    )
    name = models.CharField(
        max_length=150,
        verbose_name="Ф. И. О.",
        **NULLABLE,
    )
    comment = models.CharField(
        max_length=300,
        verbose_name="Комментарий",
        **NULLABLE,
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        **NULLABLE,
    )
    phone = models.CharField(
        max_length=20,
        **NULLABLE,
    )
    country = models.CharField(
        max_length=100,
        **NULLABLE,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        """
        Возвращает строковое представление пользователя.

        :return: Адрес электронной почты пользователя.
        """
        return self.email
