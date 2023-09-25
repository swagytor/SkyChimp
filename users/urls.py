from django.urls import path
from django.views.decorators.cache import cache_page

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegistrationView, verify_account, VerifyMessage, UserListView, \
    switch_active_status, UserDetailView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('verify_message/', VerifyMessage.as_view(), name='verify'),
    path('verification/<str:verification_code>/', verify_account, name='verification'),
    path('list/', cache_page(60)(UserListView.as_view()), name='user_list'),
    path('details/<int:pk>/', cache_page(60)(UserDetailView.as_view()), name='details'),
    path('switch_active_status/<int:pk>/', switch_active_status, name='switch_status')
]
