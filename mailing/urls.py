from django.urls import path

from .views import SendMailView
from .apps import MailingConfig

app_name = MailingConfig.name

urlpatterns = [
    path('', SendMailView.as_view(), name='send-mail'),
]
