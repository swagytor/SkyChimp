from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogCreateView, BlogDetailView, BlogUpdateView, BlogDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('', cache_page(60)(BlogListView.as_view()), name='list'),
    path('create/', BlogCreateView.as_view(), name='create'),
    path('details/<int:pk>/', BlogDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', BlogUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete')

]
