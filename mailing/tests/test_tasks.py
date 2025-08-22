from smtplib import SMTPException
from unittest.mock import MagicMock, patch

from celery.exceptions import Retry
from django.core import mail
from django.test import TestCase
from django.utils import timezone

from mailing.models import Mailing
from mailing.tasks import send_email


class TestSendEmail(TestCase):
    retries_count = 3

    def setUp(self):
        self.mailing = Mailing.objects.create(
            title='Test title',
            body='Test body',
            recipient='test@example.com',
            send_at=None,
        )

    def tearDown(self):
        self.mailing.delete()

    def test_mailing_not_exists(self):
        with self.assertRaises(Mailing.DoesNotExist):
            send_email.delay(0)

    def test_mailing_already_sent(self):
        Mailing.objects.filter(id=self.mailing.id).update(send_at=timezone.now())
        send_email.delay(self.mailing.id)
        self.assertEqual(len(mail.outbox), 0)

    def test_set_send_at(self):
        send_email.delay(self.mailing.id)

        self.mailing.refresh_from_db(fields=['send_at'])
        self.assertEqual(len(mail.outbox), 1)
        self.assertIsNotNone(self.mailing.send_at)

    @patch('mailing.tasks.django_send_mail', side_effect=SMTPException)
    def test_retry_on_error(self, mocked_send_mail: MagicMock):
        for try_number in range(self.retries_count):
            with self.assertRaisesRegex(Retry, 'Retry in 60s: SMTPException()'):
                send_email.apply(args=[self.mailing.id], retries=try_number)

    @patch('mailing.tasks.django_send_mail', side_effect=SMTPException)
    def test_retries_count_on_error(self, mocked_send_mail: MagicMock):
        with self.assertRaises(SMTPException):
            send_email.apply(args=[self.mailing.id], retries=self.retries_count)
