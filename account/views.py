import re
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView, UpdateView, TemplateView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password
from django.conf import settings
from .tokens import account_activation_token
from .forms import ConfirmPasswordForm, CustomPasswordResetForm, SignUpForm, LoginForm, LoginOTPForm, UserUpdateForm, OTPForm
from .models import User
from .otp import OTP


# NOTE: Global functions used by many views


def send_verification_email(request, user):
    current_site = request.META.get('HTTP_HOST')
    subject = 'Activate account on ' + current_site
    message = render_to_string('account_activation_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    send_mail(subject, message, 'noreply@noahdasilva.com', [user.email])


# NOTE: Views for the account app


class SignUpView(FormView):
    form_class = SignUpForm
    template_name = 'registration/sign_up.html'

    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)                     
        context["recaptcha_site_key"] = settings.RECAPTCHA_SITE_KEY
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('account'))
        return super(SignUpView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        data = self.request.POST
        username = data['username']
        email = data['email']
        password = data['password']
        
        user = User.objects.create_user(
            email=email,
            password=password, 
            username=username,
        )
        user.is_active = False
        user.save()

        if not user.is_active:
            send_verification_email(self.request, user)
            return HttpResponseRedirect(reverse_lazy('account_activation_sent'))

        return super().form_valid()


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('account')

    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)                     
        context["recaptcha_site_key"] = settings.RECAPTCHA_SITE_KEY
        return context
    
    def form_valid(self, form):
        credentials = form.cleaned_data

        user = authenticate(self.request,
            username=credentials['username'],
            password=credentials['password']
        )

        if user is not None:
            if user.otp_secret is not None:
                if 'next' in self.request.POST:
                    self.request.session['next_url'] = self.request.POST['next']
                self.request.session['username'] = credentials['username']
                self.request.session['password'] = credentials['password']                
                return HttpResponseRedirect(reverse_lazy('login_otp'))
            else:
                login(self.request, user)
            if 'next' in self.request.POST:
                return HttpResponseRedirect(self.request.POST['next'])
            else:
                return HttpResponseRedirect(self.success_url)

        else:
            messages.add_message(self.request, messages.INFO, 'Wrong credentials, please try again')
            return HttpResponseRedirect(reverse_lazy('login'))


class LoginOTPView(FormView):
    form_class = LoginOTPForm
    template_name = 'registration/login-otp.html'
    success_url = reverse_lazy('account')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.session.get('username') and not self.request.session.get('password'):
            return redirect(reverse_lazy('login'))
        return super(LoginOTPView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)                     
        context["recaptcha_site_key"] = settings.RECAPTCHA_SITE_KEY
        return context
    
    def form_valid(self, form):
        otp = form.cleaned_data['otp']
        
        username = self.request.session.get('username')
        password = self.request.session.get('password')

        user = authenticate(self.request,
            username=username,
            password=password
        )
        # Remove the session variables after authenticating the user.
        del self.request.session['username']
        del self.request.session['password']

        if OTP.verify_otp(user.otp_secret, otp):
            login(self.request, user)
            if self.request.session.get('next_url'):
                return HttpResponseRedirect(self.request.session.get('next_url'))
            else:
                return HttpResponseRedirect(self.success_url)

        else:
            messages.add_message(self.request, messages.INFO, 'Invalid 2FA code, please try again')
            return HttpResponseRedirect(reverse_lazy('login_otp'))


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('account'))


class AccountActivationSentView(TemplateView):
    template_name = 'account_activation_sent.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('account'))
        return super(AccountActivationSentView, self).dispatch(request, *args, **kwargs)


def email_verification_view(request, uidb64, token):
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


class AccountView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    model = User
    template_name = 'account.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_object(self):
        return self.request.user


class DeleteAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'delete_account.html'


@login_required
def delete_account_done_view(request):
    if request.method == 'POST':
        user = request.user

        if request.user.is_staff or request.user.is_superuser:
            return redirect(reverse_lazy('account'))
        else:
            user.delete()
            logout(request)
            
    return redirect(reverse_lazy('login'))


class ResetPasswordView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    
    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)                     
        context["recaptcha_site_key"] = settings.RECAPTCHA_SITE_KEY
        return context


class AddOTPView(LoginRequiredMixin, FormView):
    form_class = OTPForm
    model = User
    template_name = 'otp_add.html'
    success_url = reverse_lazy('account')

    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)
        context['otp_secret'] = OTP.generate_secret()
        context['qr_code'] = OTP.generate_qrcode(name=self.request.user.username, secret=context['otp_secret'])
        return context

    def form_valid(self, form):
        otp = form.cleaned_data
        otp_secret = self.request.POST.get('otp_secret', None)
        user = self.request.user
        if OTP.verify_otp(otp_secret=otp_secret, otp=otp):
            user.otp_secret = otp_secret
            user.save(update_fields=['otp_secret'])
        return super().form_valid(form)


class RemoveOTPView(LoginRequiredMixin, FormView):
    form_class = ConfirmPasswordForm
    model = User
    template_name = 'otp_remove.html'
    success_url = reverse_lazy('account')

    def get_context_data(self, **kwargs):          
        context = super().get_context_data(**kwargs)                     
        context["recaptcha_site_key"] = settings.RECAPTCHA_SITE_KEY
        return context

    def form_valid(self, form):
        form_password = form.cleaned_data['password']
        user = self.request.user

        if user.check_password(form_password):
            user.otp_secret = None
            user.save(update_fields=['otp_secret'])
            return HttpResponseRedirect(self.success_url)
        else:
            messages.add_message(self.request, messages.INFO, 'Password does not match')
            return HttpResponseRedirect(reverse_lazy('otp_remove'))