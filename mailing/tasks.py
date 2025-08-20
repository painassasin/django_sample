import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail as django_send_mail
from django.utils import timezone

from mailing.models import Mailing

logger = logging.getLogger(__name__)


@shared_task(ignore_result=True)
def send_email(mailing_id: int) -> None:
    mailing = Mailing.objects.get(id=mailing_id)
    if mailing.send_at:
        logger.warning('Mailing %s already sent', mailing_id)
        return

    result = django_send_mail(
        subject=mailing.title,
        message=mailing.body,
        recipient_list=[mailing.recipient],
        from_email=settings.DEFAULT_FROM_EMAIL,
    )
    if result == 1:
        logger.info('Mailing %s sent successfully', mailing_id)
        mailing.send_at = timezone.now()
        mailing.save(update_fields=['send_at'])
    else:
        logger.error('Mailing %s sent failed', mailing_id)
