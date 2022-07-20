from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView, UpdateView, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import socket
from .tokens import account_activation_token
from .forms import SignUpForm, LoginForm, UserUpdateForm
from .models import User


# NOTE: Global functions used by many views


def send_verification_email(request, user):
    current_site = socket.gethostname()
    subject = 'Activate Your MySite Account'
    message = render_to_string('account_activation_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    send_mail(subject, message, 'noah@noahdasilva.com', [user.email])


def redirect_to_dashboard(request):
    return redirect(reverse_lazy('dashboard'))


# NOTE: Views for the account app


class SignUpView(FormView):
    form_class = SignUpForm
    template_name = 'registration/sign_up.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('dashboard'))
        return super(SignUpView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, request):
        data = self.request.POST
        username = data['username']
        email = data['email']
        password = data['password']
        
        user = User.objects.create_user(email=email, password=password, username=username)
        user.is_active = False
        user.save()

        if not user.is_active:
            send_verification_email(request, user)
            return HttpResponseRedirect(reverse_lazy('account_activation_sent'))

        return super().form_valid()


class AccountActivationSentView(TemplateView):
    template_name = 'account_activation_sent.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('dashboard'))
        return super(AccountActivationSentView, self).dispatch(request, *args, **kwargs)


def email_verification(request, uidb64, token):
    User = get_user_model()
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect(reverse_lazy('login'))
    else:
        return HttpResponse('Activation link is invalid!')


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('/dashboard')

    def form_valid(self, form):
        credentials = form.cleaned_data

        user = authenticate(username=credentials['email'],
                            password=credentials['password'])

        if user is not None and user.is_active is False:
            send_verification_email(self.request, user)
            return HttpResponseRedirect(reverse_lazy('email_verification'))

        elif user is not None:
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


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('dashboard'))