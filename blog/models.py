

from django.db import models
from django.utils import timezone

NULLABLE = {
    'null': True,
    'blank': True
}


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='blog/', verbose_name='Изображение', **NULLABLE)
    views = models.PositiveBigIntegerField(default=0, verbose_name='Количество просмотров', **NULLABLE)
    published_at = models.DateField(default=timezone.now, verbose_name='Дата публикации', **NULLABLE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
