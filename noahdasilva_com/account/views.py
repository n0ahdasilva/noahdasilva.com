from django.shortcuts import render
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/sign-up.html'
    success_url = reverse_lazy('home')

class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'dashboard.html'
