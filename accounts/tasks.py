from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email_task(email):
  send_mail("This is the header", "And the body",
            'django@djangorocklab.com', [email], fail_silently=False)
  return None
  
