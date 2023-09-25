from django.db import models
from users.models import User

NULLABLE = {
    'blank': True,
    'null': True
}


# Create your models here.
class Client(models.Model):
    """Модель клиента"""
    email = models.EmailField(max_length=150, verbose_name='Почта', unique=True)
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    description = models.TextField(verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)

    def __str__(self):
        return f"{self.first_name} ({self.email})"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    """Модель сообщения"""
    title = models.CharField(max_length=200, verbose_name='Тема письма')
    text = models.TextField(verbose_name='Текст письма')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class MailingSettings(models.Model):
    """Модель рассылки"""
    STATUS_CREATED = 'created'
    STATUS_LAUNCHED = 'launched'
    STATUS_COMPLETE = 'complete'
    ONCE_ON_DAY = 'Раз в день'
    ONCE_ON_WEEK = 'Раз в неделю'
    ONCE_ON_MONTH = 'Раз в месяц'

    STATUS_CHOICES = [
        (STATUS_CREATED, 'Создана'),
        (STATUS_LAUNCHED, 'Запущена'),
        (STATUS_COMPLETE, 'Завершена')
    ]

    FREQUENCY_CHOICES = [
        (ONCE_ON_DAY, 'Раз в день'),
        (ONCE_ON_WEEK, 'Раз в неделю'),
        (ONCE_ON_MONTH, 'Раз в месяц')
    ]

    clients = models.ManyToManyField(Client, verbose_name='Клиенты')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)
    status = models.CharField(choices=STATUS_CHOICES, verbose_name='Статус', default=STATUS_CREATED)
    frequency = models.CharField(choices=FREQUENCY_CHOICES, verbose_name='Периодичность', default=ONCE_ON_DAY)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Письмо')
    start_date = models.DateField(verbose_name='Начало рассылки')
    end_date = models.DateField(verbose_name='Окончание рассылки')

    def __str__(self):
        return f"{self.message.title} {self.start_date}-{self.end_date}"

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingLog(models.Model):
    """Модель лога сообщения"""
    STATUS_SUCCESS = 'OK'
    STATUS_FAILED = 'Failed'

    STATUS_CHOICES = [
        (STATUS_SUCCESS, 'Успешная отправка'),
        (STATUS_FAILED, 'Ошибка отправки')
    ]

    last_try = models.DateField(auto_now_add=True, verbose_name='Последняя попытка')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Статус отправки')
    mailing_settings = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='Настройки рассылки')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')

    def __str__(self):
        return f"{self.client.email} ({self.mailing_settings.start_date} - {self.mailing_settings.end_date})"

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
