from random import shuffle, sample

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DeleteView, UpdateView, CreateView

from blog.models import Blog
from mailing.forms import MailingForm, ClientForm, MessageForm
from mailing.models import MailingSettings, Client, Message


# Mixins
class OnlyForOwnerOrSuperuserMixin:
    """Миксин на проверку доступа к чужой информации"""

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return self.object


# Simple Controllers

def index(request):
    object_list = MailingSettings.objects.all()
    client_list = Client.objects.distinct()
    blog_list = list(Blog.objects.all())

    try:
        blog_list = sample(blog_list, 3)
    except ValueError:
        blog_list = sample(blog_list, len(blog_list))

    context = {'object_list': object_list,
               'active_mailings': object_list.filter(status=MailingSettings.STATUS_LAUNCHED),
               'clients_list': client_list,
               'blog_list': blog_list
               }

    return render(request, 'mailing/homepage.html', context)


@login_required
def switch_mailing_status(request, pk):
    """Контроллер для смены статуса рассылки"""
    mailing = MailingSettings.objects.get(pk=pk)
    if mailing.status == MailingSettings.STATUS_LAUNCHED:
        mailing.status = MailingSettings.STATUS_COMPLETE
    elif mailing.status == MailingSettings.STATUS_COMPLETE:
        mailing.status = MailingSettings.STATUS_LAUNCHED
    mailing.save()
    return redirect('mailing:list')


# Creating Controllers

class MailingSettingsCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для создания настроек рассылки"""
    model = MailingSettings
    permission_required = 'mailing.add_mailing_settings'
    form_class = MailingForm
    success_url = reverse_lazy('mailing:list')

    def get_form_kwargs(self):
        """Метод для получения пользователя перед созданием форм"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Метод для проверки статуса сразу после создания"""
        self.object = form.save()
        self.object.owner = self.request.user

        if self.object.start_date <= timezone.now().date() < self.object.end_date:
            self.object.status = MailingSettings.STATUS_LAUNCHED

        return super().form_valid(form)


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для создания клиентов"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')
    permission_required = 'mailing.add_client'

    def form_valid(self, form):
        """Метод для определения пользователя после создания клиента"""
        self.object = form.save()
        self.object.owner = self.request.user

        return super().form_valid(form)


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Контроллер для создания сообщения"""
    model = Message
    success_url = reverse_lazy('mailing:list')
    form_class = MessageForm
    permission_required = 'mailing.add_message'


# Reading Controllers
class MailingSettingsListView(LoginRequiredMixin, ListView):
    """Контроллер для просмотра рассылок"""
    model = MailingSettings
    permission_required = 'mailing.view_mailing_settings'
    ordering = ('start_date',)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data['time_now'] = timezone.now().date()
        context_data['client_list'] = Client.objects.filter(owner=self.request.user)
        context_data['message_list'] = Message.objects.all()

        if self.request.user.is_staff or self.request.user.is_superuser:
            context_data['object_list'] = MailingSettings.objects.all().order_by('start_date')
        else:
            context_data['object_list'] = MailingSettings.objects.filter(owner=self.request.user).order_by('start_date')

        return context_data


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Контроллер для просмотра клиентов"""
    model = Client
    permission_required = 'mailing.view_client'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        if self.request.user.is_staff or self.request.user.is_superuser:
            context_data['object_list'] = Client.objects.all()
        else:
            context_data['object_list'] = Client.objects.filter(owner=self.request.user)

        return context_data


# Updating Controllers

class MailingSettingsUpdateView(LoginRequiredMixin, OnlyForOwnerOrSuperuserMixin, UpdateView):
    """Контроллер для изменения рассылок"""
    model = MailingSettings
    permission_required = 'mailing.change_mailing_settings'
    form_class = MailingForm
    success_url = reverse_lazy('mailing:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ClientUpdateView(LoginRequiredMixin, OnlyForOwnerOrSuperuserMixin, UpdateView):
    """Контроллер для изменения клиентов"""
    model = Client
    permission_required = 'mailing.change_client'
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')


# Deleting Controllers


class MailingSettingsDeleteView(LoginRequiredMixin, OnlyForOwnerOrSuperuserMixin, DeleteView):
    """Контроллер для удаления рассылок"""
    model = MailingSettings
    permission_required = 'mailing.delete_mailing_settings'
    success_url = reverse_lazy('mailing:list')


class ClientDeleteView(LoginRequiredMixin, OnlyForOwnerOrSuperuserMixin, DeleteView):
    """Контроллер для удаления клиентов"""
    model = Client
    permission_required = 'mailing.delete_client'
    success_url = reverse_lazy('mailing:client_list')
