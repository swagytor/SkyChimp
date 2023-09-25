from django.core.mail import send_mail

from config import settings


def send_verification_message(verification_url, email):
    print(settings.EMAIL_HOST_USER)
    send_mail(
        subject='SkyChimp - Подтверждение электронной почты',
        message=f"Приветствуем!\n\n"
                f"Для подтверждения электронной почты и завершения процесса регистрации, пройдите, пожалуйста, "
                f"по ссылке:\n"
                f"{verification_url}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
