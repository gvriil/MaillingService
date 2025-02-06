from django.db import models
from config import settings
from config.settings import NULLABLE


class Client(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    comment = models.CharField(max_length=256, **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE
    )

    def __str__(self):
        return self.email

    class Meta:
        ordering = ["email"]
