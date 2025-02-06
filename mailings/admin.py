from django.contrib import admin
from .models import Mailing, Attempt

# Регистрация моделей в административной панели
admin.site.register(Mailing)
admin.site.register(Attempt)
