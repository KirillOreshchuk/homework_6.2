import random

from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView

from config import settings
from users.forms import UserRegisterForm, UserForm
from users.models import User


class LoginView(BaseLoginView):
    """
    Контроллер, который отвечает за вход в профиль
    """
    template_name = 'users/login.html'
    success_url = reverse_lazy('catalog:home_page')


class LogoutView(BaseLogoutView):
    """
    Контроллер, который отвечает за выход из профиля
    """
    model = User
    success_url = reverse_lazy('catalog:home_page')


class RegisterView(CreateView):
    """
    Контроллер, который отвечает регистрацию профиля
    """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:code')
    template_name = 'users/register.html'

    def form_valid(self, form):
        new_pass = ''.join([str(random.randint(0, 9)) for _ in range(5)])
        new_user = form.save(commit=False)
        new_user.code = new_pass
        new_user.save()

        send_mail(
            subject='Регистрация на платформе',
            message=f"Ваш код подтверждения: {new_user.code}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )

        return super().form_valid(form)


class UserConfirmEmailView(View):
    """
    Контроллер, который отвечает за подтверждение профиля через код верификации
    """
    model = User
    template_name = 'users/code.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        code = request.POST.get('code')
        user = User.objects.filter(code=code).first()

        if user is not None and user.code == code:
            user.is_active = True
            user.save()
            return redirect('users:login')


class UserUpdateView(UpdateView):
    """
    Контроллер, который отвечает за изменение профиля
    """
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    """
    Генерирует новый пароль и отпраляет на почту
    """
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    send_mail(
        subject='Регистрация на платформе',
        message=f"Ваш новый пароль {new_password}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )

    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('users:login'))
