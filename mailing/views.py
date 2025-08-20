from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView

from mailing.forms import MailingForm


class SendMailView(CreateView):
    form_class = MailingForm
    template_name = 'mailing/send_mail.html'
    success_url = reverse_lazy('mailing:send-mail')

    def form_valid(self, form: MailingForm) -> HttpResponse:
        mailing = form.save()

        send_mail(
            subject=mailing.title,
            message=mailing.body,
            recipient_list=[mailing.recipient],
            from_email=settings.DEFAULT_FROM_EMAIL,
        )
        messages.success(self.request, 'Сообщение отправлено')

        mailing.send_at = timezone.now()
        mailing.save(update_fields=['send_at'])

        return redirect(self.success_url)
