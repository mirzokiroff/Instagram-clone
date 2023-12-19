from random import randint

from django.core.cache import cache
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from conf.celery import app
from conf import settings
from conf.settings import EMAIL_HOST_USER


@app.task
def send_to_gmail(email):
    print('ACCEPT TASK')
    print(email)
    otp_code = str(randint(1000, 9999))  # Generate a 4-digit OTP code
    cache.set(f'{settings.CACHE_KEY_PREFIX}:{otp_code}', email, timeout=settings.CACHE_TTL)
    subject = 'Activate your account'

    message = render_to_string(f'email_template.html', {'code': otp_code})

    recipient_list = [email]

    email = EmailMessage(subject, message, EMAIL_HOST_USER, recipient_list)
    email.content_subtype = 'html'
    result = email.send()
    print('Send to MAIL')
    return result
