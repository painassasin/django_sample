from typing import Any, ClassVar

from django import forms

from mailing.models import Mailing


class BootstrapFormStylesMixin:
    fields: ClassVar[dict]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MailingForm(BootstrapFormStylesMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('title', 'body', 'recipient')
        widgets = {
            'body': forms.Textarea(attrs={'rows': 5}),
        }
        labels = {'title': 'Тема', 'body': 'Содержимое', 'recipient': 'Получатель'}
