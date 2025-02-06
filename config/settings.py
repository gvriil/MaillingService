"""
Настройки Django для проекта config.

Сгенерировано с помощью 'django-admin startproject' с использованием Django 5.0.4.

Для получения дополнительной информации о данном файле см.:
https://docs.djangoproject.com/en/5.0/topics/settings/

Для полного списка настроек и их значений см.:
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Построение путей внутри проекта, например: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")  # Загрузка переменных окружения из файла .env

# Настройки для быстрого старта разработки — не подходят для production.
# Подробнее: https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# ВНИМАНИЕ БЕЗОПАСНОСТИ: держите секретный ключ в секрете при использовании в production!
SECRET_KEY = "django-insecure-h&armrt#s_a-8wyu4%5&249sdke4(q5da0lw5*(dnr(5_o0kif"

# ВНИМАНИЕ БЕЗОПАСНОСТИ: не запускайте с включенным DEBUG в production!
DEBUG = True

ALLOWED_HOSTS = []  # Список разрешенных хостов

# Определение установленных приложений
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "mailings",
    "users",
    "clients",
    "django_crontab",
    "blogpost",
    "user_messages",
    "django_apscheduler",
]

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25

# Определение промежуточного ПО (middleware)
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Корневой конфигурационный файл URL
ROOT_URLCONF = "config.urls"

# Настройки шаблонов
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "clients/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI-приложение
WSGI_APPLICATION = "config.wsgi.application"

# Настройки базы данных
# Подробнее: https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "default_db_name"),  # Имя базы данных
        "USER": os.getenv("DB_USER", "default_user"),  # Пользователь базы данных
        "PASSWORD": os.getenv("DB_PASSWORD", "default_password"),  # Пароль
        "HOST": os.getenv("DB_HOST", "localhost"),  # Хост
        "PORT": os.getenv("DB_PORT", "5432"),  # Порт
    }
}

# Валидаторы паролей
# Подробнее: https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Настройки интернационализации
LANGUAGE_CODE = "en-us"  # Язык по умолчанию
TIME_ZONE = "Europe/Moscow"  # Временная зона
USE_I18N = True  # Включение интернационализации
USE_TZ = True  # Использование временных зон

# Настройки статических файлов (CSS, JavaScript, Images)
# Подробнее: https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Настройки медиафайлов
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Тип поля для первичного ключа по умолчанию
# Подробнее: https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Модель пользователя
AUTH_USER_MODEL = "users.User"

# Настройки перенаправлений
LOGOUT_REDIRECT_URL = "login"  # Перенаправление после выхода
LOGIN_URL = "login"  # URL для входа
LOGIN_REDIRECT_URL = 'mailings:home'  # Перенаправление на главную страницу после входа
# Настройки cron-задач
CRONJOBS = [("*/5 * * * *", "mailings.tasks.send_mails")]

# Настройки электронной почты
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.yandex.ru")  # Хост SMTP
EMAIL_PORT = os.getenv("EMAIL_PORT", 465)  # Порт SMTP
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")  # Пользователь SMTP
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")  # Пароль SMTP
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "False") == "True"  # Использование TLS
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "True") == "True"  # Использование SSL
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # Адрес отправителя по умолчанию

# Дополнительные параметры для полей моделей
NULLABLE = {"blank": True, "null": True}

CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Путь к Redis
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}