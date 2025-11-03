from django.contrib.auth.models import AbstractUser
from django.db import models

# Можно использовать стандартную модель User или расширить её
# Здесь пример расширенной модели (опционально)

# class CustomUser(AbstractUser):
#     """Расширенная модель пользователя"""
#     bio = models.TextField(max_length=500, blank=True)
#     phone_number = models.CharField(max_length=20, blank=True)
#
#     class Meta:
#         db_table = 'users'
#         verbose_name = 'Пользователь'
#         verbose_name_plural = 'Пользователи'

# Если используешь CustomUser, добавь в settings.py:
# AUTH_USER_MODEL = 'users.CustomUser'
