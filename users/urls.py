from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, generate_new_password, UserConfirmEmailView, UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
   path('', LoginView.as_view(), name='login'),
   path('logout/', LogoutView.as_view(), name='logout'),
   path('register/', RegisterView.as_view(), name='register'),
   path('code/', UserConfirmEmailView.as_view(), name='code'),
   path('profile', UserUpdateView.as_view(), name='profile'),
   path('generate_new_password/', generate_new_password, name='generate_new_password')
]
