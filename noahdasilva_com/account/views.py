from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.contrib import messages
from .forms import SignUpForm, LoginForm, NewPasswordForm
from .models import User


class SignUpView(FormView):
    form_class = SignUpForm
    template_name = 'registration/sign-up.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        login(self.request, user)
        if user is not None:
            return HttpResponseRedirect(self.success_url)

        return super().form_valid(form)


class LoginView(FormView):
    form_class = LoginForm
    success_url = reverse_lazy('dashboard')
    template_name = 'registration/login.html'

    def form_valid(self, form):
        credentials = form.cleaned_data

        user = authenticate(username=credentials['email'],
                            password=credentials['password'])

        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(self.success_url)

        else:
            messages.add_message(self.request, messages.INFO, 'Wrong credentials\
                                please try again')
            return HttpResponseRedirect(reverse_lazy('login'))


class DashboardView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = 'dashboard.html'


def Logout(request):
    logout(request)
    return redirect(reverse_lazy('dashboard'))