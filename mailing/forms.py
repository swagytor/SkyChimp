from django import forms
from django.utils import timezone

from mailing.models import MailingSettings, Client, Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFormMixin, forms.ModelForm):
    clients = forms.ModelMultipleChoiceField(
        label='Получатели',
        queryset=Client.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2'})
    )

    class Meta:
        model = MailingSettings
        exclude = ('status', 'owner')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user.is_superuser:
            self.fields['clients'].queryset = Client.objects.all()
        elif user:
            self.fields['clients'].queryset = Client.objects.filter(owner=user)
        else:
            self.fields['clients'].queryset = Client.objects.none()

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data['start_date']
        end_date = cleaned_data['end_date']
        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError('Дата окончания должна быть больше даты начала!')
            elif end_date <= timezone.now().date():
                raise forms.ValidationError('Дата окончания должна быть больше текущей даты!')

        return cleaned_data


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('owner',)

class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
