from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from mailing.forms import MailingForm
from mailing.tasks import send_email


class SendMailView(CreateView):
    form_class = MailingForm
    template_name = 'mailing/send_mail.html'
    success_url = reverse_lazy('mailing:send-mail')

    def form_valid(self, form: MailingForm) -> HttpResponse:
        mailing = form.save()
        send_email.delay(mailing.id)
        messages.success(self.request, 'Сообщение отправлено')
        return redirect(self.success_url)
