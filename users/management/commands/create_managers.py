# users/management/commands/create_managers.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from users.models import User  # Импортируйте вашу кастомную модель пользователя
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Create managers and add them to the "Менеджеры" group'

    def handle(self, *args, **kwargs):
        # Создаем группу "Менеджеры", если она не существует
        managers_group, created = Group.objects.get_or_create(name='Менеджеры')

        # Запрашиваем данные пользователя через input
        email = input("Enter email: ")
        password = input("Enter password: ")

        # Генерируем username на основе email
        username = email.split('@')[0]

        try:
            # Проверяем, существует ли пользователь с таким email
            user, created = User.objects.get_or_create(email=email, defaults={'username': username})
            if created:
                user.set_password(password)
                user.is_staff = False
                user.is_superuser = False
                user.save()
                user.groups.add(managers_group)
                self.stdout.write(self.style.SUCCESS(f'Successfully created user {user.email} and added to "Менеджеры" group'))
            else:
                self.stdout.write(self.style.WARNING(f'User {user.email} already exists'))
                # Добавляем пользователя в группу, если он уже существует и не состоит в ней
                if not user.groups.filter(name='Менеджеры').exists():
                    user.groups.add(managers_group)
                    self.stdout.write(self.style.SUCCESS(f'User {user.email} added to "Менеджеры" group'))
        except IntegrityError as e:
            self.stdout.write(self.style.ERROR(f'Error creating user: {e}'))

        self.stdout.write(self.style.SUCCESS('Managers creation completed'))
