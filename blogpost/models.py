from config.settings import NULLABLE
from django.utils import timezone
from django.conf import settings
from django.db import models


class BlogPost(models.Model):
    """Модель для представления блог-поста."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    preview = models.ImageField(upload_to="blog_previews/", blank=True)
    is_published = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_posts", blank=True
    )

    def __str__(self):
        """Возвращает строковое представление блог-поста."""
        return self.title


class Comment(models.Model):
    """Модель для представления комментария к блог-посту."""

    blogpost = models.ForeignKey(
        BlogPost, related_name="comments", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="user_comments",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_comments", blank=True
    )

    def __str__(self):
        """Возвращает строковое представление комментария."""
        return f"Comment by {self.author} on {self.blogpost}"
