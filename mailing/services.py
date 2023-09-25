import os
from datetime import datetime

from django.core.mail import send_mail
from django.db.models import Q

import config.settings
from mailing.models import MailingLog, MailingSettings


def send_email(mailing_settings, client):
    """Функция отправки сообщения и создания лога"""
    result = send_mail(
        subject=mailing_settings.message.title,
        message=mailing_settings.message.text,
        from_email=config.settings.EMAIL_HOST_USER,
        recipient_list=[client.email],
        fail_silently=False
    )

    MailingLog.objects.create(
        status=(MailingLog.STATUS_SUCCESS if result else MailingLog.STATUS_FAILED),
        mailing_settings=mailing_settings,
        client_id=client.pk
    )


def send_mails():
    """Функция фильтрации рассылок, с последующей сменой статуса и отправкой сообщения каждому пользователю"""
    date_now = datetime.now().date()

    # получаем список всех созданных и активных рассылок
    for mailing in MailingSettings.objects.filter(Q(status=MailingSettings.STATUS_CREATED) |
                                                  Q(status=MailingSettings.STATUS_LAUNCHED)):

        # проверяем дату окончания у рассылки для выставления статуса "Завершён"
        if date_now > mailing.end_date:
            mailing.status = MailingSettings.STATUS_COMPLETE

        # проверяем дату начала рассылки для выставления статуса "Активен"
        elif date_now >= mailing.start_date:
            mailing.status = MailingSettings.STATUS_LAUNCHED

            # проходимся по каждому клиенту рассылки
            for mailing_client in mailing.clients.all():
                # получаем лог КОНКРЕТНОГО пользователя КОНКРЕТНОЙ рассылки
                mailing_log = MailingLog.objects.filter(client=mailing_client, mailing_settings=mailing)

                # если существуют логи, находим самый недавний, и проверяем на количество пройденного времени
                if mailing_log.exists():
                    last_try_date = mailing_log.order_by('-last_try').first().last_try

                    if mailing.frequency == MailingSettings.ONCE_ON_DAY:
                        if (date_now - last_try_date).days >= 1:
                            send_email(mailing, mailing_client)

                    elif mailing.frequency == MailingSettings.ONCE_ON_WEEK:
                        if (date_now - last_try_date).days >= 7:
                            send_email(mailing, mailing_client)

                    elif mailing.frequency == MailingSettings.ONCE_ON_MONTH:
                        if (date_now - last_try_date).days >= 30:
                            send_email(mailing, mailing_client)
                else:
                    send_email(mailing, mailing_client)
        mailing.save()
