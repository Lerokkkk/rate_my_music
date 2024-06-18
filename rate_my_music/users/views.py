from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Prefetch
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from .forms import LoginUserForm, RegistrationUserForm
from main.models import Rate, Artist


# Create your views here.


class Profile(ListView):
    template_name = 'users/profile.html'
    context_object_name = 'q'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        # print(context)
        return context

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return Rate.objects.filter(user=self.get_object()).select_related('composition').prefetch_related('composition__artist')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login_user.html'
    next_page = reverse_lazy('home')
    extra_context = {'title': 'Вход'}


class RegistrationUser(CreateView):
    template_name = 'users/registration.html'
    form_class = RegistrationUserForm
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')