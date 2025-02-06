"""
ASGI-конфигурация для проекта config.

Он предоставляет ASGI-приложение как переменную уровня модуля с именем ``application``.

Для получения дополнительной информации об этом файле см.:
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Установка переменной окружения для указания модуля настроек Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Создание ASGI-приложения
application = get_asgi_application()