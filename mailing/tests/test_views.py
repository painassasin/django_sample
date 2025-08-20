from unittest.mock import MagicMock, patch

from django.contrib.messages import constants as messages_constants, get_messages
from django.test import TestCase
from django.urls import reverse_lazy

from mailing.models import Mailing


class TestSendMailView(TestCase):
    url = reverse_lazy('mailing:send-mail')
    form_data = {
        'title': 'Test title',
        'body': 'Test body',
        'recipient': 'test@example.com',
    }

    def test_redirect_to_the_same_url(self):
        response = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.url)

    def test_create_new_mailing_object(self):
        self.client.post(self.url, self.form_data)

        mailing = Mailing.objects.get()
        self.assertEqual(mailing.title, self.form_data['title'])
        self.assertEqual(mailing.body, self.form_data['body'])
        self.assertEqual(mailing.recipient, self.form_data['recipient'])
        self.assertIsNotNone(mailing.send_at)

    def test_add_message_to_template(self):
        response = self.client.post(self.url, self.form_data)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, 'Сообщение отправлено')
        self.assertEqual(messages[0].level, messages_constants.SUCCESS)

    @patch('mailing.views.send_email')
    def test_send_email(self, send_email_mock: MagicMock):
        self.client.post(self.url, self.form_data)
        mailing = Mailing.objects.get()
        send_email_mock.delay.assert_called_once_with(mailing.id)
