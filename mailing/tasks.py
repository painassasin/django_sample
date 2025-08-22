import logging
from smtplib import SMTPException

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail as django_send_mail
from django.utils import timezone

from mailing.models import Mailing

logger = logging.getLogger(__name__)


@shared_task(
    ignore_result=True,
    autoretry_for=(SMTPException,),
    max_retries=3,
    default_retry_delay=60,
)
def send_email(mailing_id: int) -> None:
    mailing = Mailing.objects.get(id=mailing_id)
    if mailing.send_at:
        logger.warning('Mailing %s already sent', mailing_id)
        return

    django_send_mail(
        subject=mailing.title,
        message=mailing.body,
        recipient_list=[mailing.recipient],
        from_email=settings.DEFAULT_FROM_EMAIL,
        fail_silently=False,
    )
    logger.info('Mailing %s sent successfully', mailing_id)
    mailing.send_at = timezone.now()
    mailing.save(update_fields=['send_at'])
