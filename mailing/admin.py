from django.contrib import admin

from mailing.models import Message, Client, MailingSettings, MailingLog


# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title')
    search_fields = ('title',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'first_name', 'last_name')
    search_fields = ('email', 'first_name', 'last_name',)


@admin.register(MailingSettings)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'message', 'frequency', 'start_date', 'end_date', 'status')
    filter_horizontal = ('clients',)


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('last_try', 'status', 'mailing_settings', 'client',)
