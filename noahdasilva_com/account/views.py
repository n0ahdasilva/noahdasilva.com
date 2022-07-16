from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import FormView, UpdateView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import SignUpForm, LoginForm, UserUpdateForm
from .models import User


class SignUpView(FormView):
    form_class = SignUpForm
    template_name = 'registration/sign_up.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super(SignUpView, self).dispatch(request, *args, **kwargs)

    # NOTE: This is a hack to get the form to hash the passwords.
    # Not sure if this is the best way to do this.
    def form_valid(self, request):
        data = self.request.POST
        username = data['username']
        email = data['email']
        password = data['password']
        
        user = User.objects.create_user(email=email, password=password, username=username)
        user.save()

        login(self.request, user)
        if user is not None:
            return HttpResponseRedirect('/dashboard')

        return super().form_valid()
'''
    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        login(self.request, user)
        if user is not None:
            return HttpResponseRedirect('/dashboard')

        return super().form_valid(form)
'''


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('/dashboard')

    def form_valid(self, form):
        credentials = form.cleaned_data

        user = authenticate(username=credentials['email'],
                            password=credentials['password'])

        if user is not None:
            login(self.request, user)
            if 'next' in self.request.POST:
                return HttpResponseRedirect(self.request.POST['next'])
            else:
                return HttpResponseRedirect(self.success_url)

        else:
            messages.add_message(self.request, messages.INFO, 'Wrong credentials please try again')
            return HttpResponseRedirect(reverse_lazy('login'))


class DashboardView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    model = User
    template_name = 'dashboard.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_object(self):
        return self.request.user


def Logout(request):
    logout(request)
    return redirect(reverse_lazy('dashboard'))