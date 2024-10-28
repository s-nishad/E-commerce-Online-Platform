from django.urls import path

from accounts.views import register_view, login_view, get_all_users

app_name = 'accounts'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('users/', get_all_users, name='users'),
]
