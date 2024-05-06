from django.contrib.auth.models import AbstractUser
import uuid
from django.db import models


class User(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователь"
