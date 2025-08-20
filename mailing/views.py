from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from mailing.forms import MailingForm


class SendMailView(CreateView):
    form_class = MailingForm
    template_name = 'mailing/send_mail.html'
    success_url = reverse_lazy('mailing:send-mail')

    def form_valid(self, form: MailingForm) -> HttpResponse:
        response = super().form_valid(form)

        send_mail(
            subject=self.object.title,
            message=self.object.body,
            recipient_list=[self.object.recipient],
            from_email=settings.DEFAULT_FROM_EMAIL,
        )
        messages.success(self.request, 'Сообщение отправлено')
        return response
