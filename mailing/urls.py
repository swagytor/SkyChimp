from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import index, MailingSettingsListView, MailingSettingsCreateView, \
    MailingSettingsUpdateView, MailingSettingsDeleteView, ClientListView, ClientCreateView, \
    ClientUpdateView, ClientDeleteView, MessageCreateView, switch_mailing_status

app_name = MailingConfig.name

urlpatterns = [
    path('', index, name='homepage'),
    # MailingSetting's urls
    path('mailings/', cache_page(60)(MailingSettingsListView.as_view()), name='list'),
    path('create/', MailingSettingsCreateView.as_view(), name='create'),
    path('update/<int:pk>/', MailingSettingsUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', MailingSettingsDeleteView.as_view(), name='delete'),
    path('switch_mailing_status/<int:pk>/', switch_mailing_status, name='switch_status'),

    # Client's urls
    path('clients/', cache_page(60)(ClientListView.as_view()), name='client_list'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    # Message's urls
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
]
