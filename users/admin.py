from django.contrib import admin

from users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ['password']
# Регистрация модели User в административной панели Django
# admin.site.register(User)
