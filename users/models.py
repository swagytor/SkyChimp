from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {
    'blank': True,
    'null': True
}

# Create your models here.


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')

    avatar = models.ImageField(upload_to='users/', default='users/noname.jpg', **NULLABLE, verbose_name='Аватар')
    is_active = models.BooleanField(default=False, verbose_name='Активен')
    verification_code = models.CharField(max_length=10, unique=True, **NULLABLE, verbose_name='Код верификации')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
