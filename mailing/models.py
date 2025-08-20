from django.db import models


class Mailing(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    recipient = models.EmailField()
    send_at = models.DateTimeField(null=True, blank=True)
