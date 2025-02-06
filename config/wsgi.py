"""
WSGI config for config project.

Этот файл предоставляет WSGI callable в виде переменной уровня модуля с именем ``application``.

Для получения дополнительной информации об этом файле, смотрите
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Получаем WSGI-приложение
application = get_wsgi_application()
