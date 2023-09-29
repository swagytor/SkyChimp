from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from blog.forms import BlogForm
from blog.models import Blog


# Create your views here.

class BlogCreateView(PermissionRequiredMixin, CreateView):
    """
    Контроллер для создания объекта Blog
    """
    model = Blog
    permission_required = 'blog.add_blog'
    success_url = reverse_lazy('blog:list')
    form_class = BlogForm


class BlogListView(ListView):
    """
    Контроллер для просмотра объектов Blog
    """
    model = Blog

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data['user'] = self.request.user

        return context_data


class BlogDetailView(DetailView):
    """
    Контроллер для просмотра отдельного объекта Blog
    """
    model = Blog

    def get_object(self, queryset=None):
        """Метод для прибавки просмотров блога"""
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()

        return self.object


class BlogUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Контроллер для обновления объекта Blog
    """
    model = Blog
    permission_required = 'blog.change_blog'
    success_url = reverse_lazy('blog:list')
    form_class = BlogForm


class BlogDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Контроллер для Удаления объекта Blog
    """
    model = Blog
    permission_required = 'blog.delete_blog'
    success_url = reverse_lazy('blog:list')
