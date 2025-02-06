from django.contrib import admin
from .models import BlogPost, Comment


# Регистрация модели BlogPost
admin.site.register(BlogPost)

# Регистрация модели Comment
admin.site.register(Comment)
