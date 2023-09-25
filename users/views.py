import secrets

from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, ListView, DetailView

from users import services
from users.forms import UserAuthForm, UserRegisterForm
from users.models import User


# Create your views here.
class RegistrationView(CreateView):
    model = User
    success_url = reverse_lazy('users:verify')
    template_name = 'users/register.html'

    form_class = UserRegisterForm

    def form_valid(self, form):
        if form.is_valid():
            instance = form.save()
            verification_code = secrets.token_urlsafe(nbytes=7)
            instance.verification_code = verification_code

            url = reverse('users:verification', args=[verification_code])
            total_url = self.request.build_absolute_uri(url)
            services.send_verification_message(total_url, instance.email)

            instance.save()
        return super().form_valid(form)


class VerifyMessage(TemplateView):
    template_name = 'users/verify_message.html'


def verify_account(request, verification_code):
    user = User.objects.get(verification_code=verification_code)
    user.is_active = True
    user.verification_code = None
    user.save()
    return redirect(reverse('users:login'))


class LoginView(BaseLoginView):
    template_name = 'users/login.html'
    form_class = UserAuthForm
    success_url = reverse_lazy('mailing:list')


class LogoutView(BaseLogoutView):
    pass


class UserListView(ListView):
    model = User
    ordering = ('pk',)

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context_data['object_list'] = User.objects.exclude(is_superuser=True)
        elif self.request.user.is_staff:
            context_data['object_list'] = User.objects.exclude(is_staff=True)

        return context_data


class UserDetailView(DetailView):
    model = User


def switch_active_status(request, pk):
    user = User.objects.get(pk=pk)
    user.is_active = not user.is_active
    user.save()
    return redirect('users:user_list')
