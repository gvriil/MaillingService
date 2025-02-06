"""
URL конфигурация для проекта config.

Список `urlpatterns` маршрутизирует URL-адреса к представлениям. Для получения дополнительной информации смотрите:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Примеры:
Функциональные представления
    1. Добавьте импорт:  from my_app import views
    2. Добавьте URL в urlpatterns:  path('', views.home, name='home')
Классовые представления
    1. Добавьте импорт:  from other_app.views import Home
    2. Добавьте URL в urlpatterns:  path('', Home.as_view(), name='home')
Включение другого URLconf
    1. Импортируйте функцию include(): from django.urls import include, path
    2. Добавьте URL в urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from config import settings
from mailings.views import home
from users.views import profile

urlpatterns = [
    path("admin/", admin.site.urls),  # Административная панель
    path("users/profile/", profile, name="profile"),  # Профиль пользователя
    path("users/", include("users.urls", namespace="users")),  # URL-адреса для приложения пользователей
    path("clients/", include("clients.urls", namespace="clients")),  # URL-адреса для приложения клиентов
    path("mailings/", include("mailings.urls", namespace="mailings")),  # URL-адреса для приложения рассылок
    path("user_messages/", include("user_messages.urls", namespace="user_messages")),  # URL-адреса для приложения сообщений пользователей
    path("blog/", include("blogpost.urls", namespace="blogpost")),  # URL-адреса для блога
    path("", home, name="home"),
    path("redirect/", RedirectView.as_view(url="users/login/", permanent=False), name="redirect"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Обслуживание медиафайлов в режиме отладки
