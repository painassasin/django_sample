from django.urls import path

from .apps import MailingConfig
from .views import SendMailView

app_name = MailingConfig.name

urlpatterns = [
    path('', SendMailView.as_view(), name='send-mail'),
]
