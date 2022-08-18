from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth import forms as auth_forms
import requests
import re
from django.contrib.auth.hashers import check_password 
from django.conf import settings
from .otp import OTP


#NOTE: Global variables


MIN_PASS_LENGTH = 8
MAX_PASS_LENGTH = 128

MIN_USER_LENGTH = 4
MAX_USER_LENGTH = 24

MIN_NAME_LENGTH = 2
MAX_NAME_LENGTH = 64


# NOTE: Forms for the account app


class SignUpForm(forms.ModelForm):
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    recaptcha = forms.CharField(
        widget=forms.HiddenInput(),
        max_length=1024,
        required=False
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password',]

    def clean_username(self):
        username = self.cleaned_data['username']
        
        # Must be between 4 and 24 characters long
        if len(username) < MIN_USER_LENGTH or len(username) > MAX_USER_LENGTH:
            raise forms.ValidationError("Username must be between %d and %d characters " \
                "long." % (MIN_USER_LENGTH, MAX_USER_LENGTH))

        # Only allows for alphanumeric characters and underscores
        if re.search(r'[^a-zA-Z0-9_]', username) is not None:
            raise forms.ValidationError(
                "Username can only contain letters, numbers, and underscores.")

        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')

        # Must be between 8 and 128 characters long
        if len(password) < MIN_PASS_LENGTH or len(password) > MAX_PASS_LENGTH:
            raise forms.ValidationError("Password must be between %d and %d characters " \
                "long." % (MIN_PASS_LENGTH, MAX_PASS_LENGTH))

        # searching for digits
        digit_error = re.search(r"\d", password) is None
        # searching for uppercase
        uppercase_error = re.search(r"[A-Z]", password) is None
        # searching for lowercase
        lowercase_error = re.search(r"[a-z]", password) is None
        # searching for symbols
        symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None

        # overall result
        password_valid = not (digit_error or uppercase_error or lowercase_error or symbol_error)
        
        if not password_valid:
            raise forms.ValidationError(
                "The new password must contain at least one letter, number, and special character.")

        return password

    def clean_recaptcha(self):
        cleaned_data = super(SignUpForm, self).clean()
        recaptcha_response = cleaned_data.get('recaptcha')
        data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post(settings.RECAPTCHA_URL, data=data)
        result = r.json()

        if result.get('success') and result.get('score') > 0.5:
            # client is human
            pass
        else:
            raise forms.ValidationError('reCAPTCHA verification failed, please try again.')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    recaptcha = forms.CharField(
        widget=forms.HiddenInput(),
        max_length=1024,
        required=False
    )

    def clean_recaptcha(self):
        cleaned_data = super(LoginForm, self).clean()
        recaptcha_response = cleaned_data.get('recaptcha')
        data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post(settings.RECAPTCHA_URL, data=data)
        result = r.json()

        if result.get('success') and result.get('score') > 0.5:
            # client is human
            pass
        else:
            raise forms.ValidationError('reCAPTCHA verification failed, please try again.')


class LoginOTPForm(forms.Form):
    otp = forms.CharField(max_length=6)
    recaptcha = forms.CharField(
        widget=forms.HiddenInput(),
        max_length=1024,
        required=False
    )

    def clean_recaptcha(self):
        cleaned_data = super(LoginOTPForm, self).clean()
        recaptcha_response = cleaned_data.get('recaptcha')
        data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post(settings.RECAPTCHA_URL, data=data)
        result = r.json()

        if result.get('success') and result.get('score') > 0.5:
            # client is human
            pass
        else:
            raise forms.ValidationError('reCAPTCHA verification failed, please try again.')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'full_name', 'email',]

    def clean_username(self):
        username = self.cleaned_data['username']

        # Must be between 4 and 24 characters long
        if len(username) < MIN_USER_LENGTH or len(username) > MAX_USER_LENGTH:
            raise forms.ValidationError("Username must be between %d and %d characters " \
                "long." % (MIN_USER_LENGTH, MAX_USER_LENGTH))

        # Only allows for alphanumeric characters and underscores
        if re.search(r'[^a-zA-Z0-9_]', username) is not None:
            raise forms.ValidationError(
                "Username can only contain letters, numbers, and underscores.")

        return username

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')

        # Check if user currently has a name
        if full_name is None:
            return full_name

        # Must be between 2 and 64 characters long
        if  len(full_name) < MIN_NAME_LENGTH or len(full_name) > MAX_NAME_LENGTH:
            raise forms.ValidationError("Name must be between %d and %d characters " \
                "long." % (MIN_NAME_LENGTH, MAX_NAME_LENGTH))

        # Only allow letters, dashs, and spaces
        if re.search(r'[^a-zA-Z- ]', full_name) is not None:
            raise forms.ValidationError(
                "Name can only contain letters, dashs, and spaces.")
            
        return full_name


class CustomPasswordResetForm(auth_forms.PasswordResetForm):
    recaptcha = forms.CharField(
        widget=forms.HiddenInput(),
        max_length=1024,
        required=False
    )

    def clean(self):
        cleaned_data = super(CustomPasswordResetForm, self).clean()
        recaptcha_response = cleaned_data.get('recaptcha')
        data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post(settings.RECAPTCHA_URL, data=data)
        result = r.json()
        if result.get('success') and result.get('score') > 0.5:
            # client is human
            pass
        else:
            raise forms.ValidationError('reCAPTCHA verification failed, please try again.')


class CustomSetPasswordForm(auth_forms.SetPasswordForm):
    def clean_new_password2(self):
        password = self.cleaned_data.get('new_password2')
        first_password = self.cleaned_data.get('new_password1')

        # Passwords must match
        if password != first_password:
            raise auth_forms.ValidationError("Passwords do not match.")
        
        # Must be between 8 and 128 characters long
        if len(password) < MIN_PASS_LENGTH or len(password) > MAX_PASS_LENGTH:
            raise auth_forms.ValidationError("Password must be between %d and %d characters " \
                " long." % (MIN_PASS_LENGTH, MAX_PASS_LENGTH))

        # searching for digits
        digit_error = re.search(r"\d", password) is None
        # searching for uppercase
        uppercase_error = re.search(r"[A-Z]", password) is None
        # searching for lowercase
        lowercase_error = re.search(r"[a-z]", password) is None
        # searching for symbols
        symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None

        # overall result
        password_valid = not (digit_error or uppercase_error or lowercase_error or symbol_error)

        if not password_valid:
            raise auth_forms.ValidationError(
                "The new password must contain at least one letter, number, and special character.")

        return password


class CustomPasswordChangeForm(auth_forms.PasswordChangeForm):
    def clean_new_password2(self):
        password = self.cleaned_data.get('new_password2')
        old_password = self.cleaned_data.get('old_password')

        # Must be new password
        if password == old_password:
            raise auth_forms.ValidationError(
                "New password must be different from old password.")

        # Must be between 8 and 128 characters long
        if len(password) < MIN_PASS_LENGTH or len(password) > MAX_PASS_LENGTH:
            raise auth_forms.ValidationError("Password must be between %d and %d characters " \
                "long." % (MIN_PASS_LENGTH, MAX_PASS_LENGTH))

        # searching for digits
        digit_error = re.search(r"\d", password) is None
        # searching for uppercase
        uppercase_error = re.search(r"[A-Z]", password) is None
        # searching for lowercase
        lowercase_error = re.search(r"[a-z]", password) is None
        # searching for symbols
        symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None

        # overall result
        password_valid = not (digit_error or uppercase_error or lowercase_error or symbol_error)

        if not password_valid:
            raise auth_forms.ValidationError(
                "The new password must contain at least one letter, number, and special character.")

        return password


class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)
    otp_secret = forms.CharField(max_length=64, widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super(OTPForm, self).clean()
        otp = cleaned_data.get('otp')
        otp_secret = cleaned_data.get('otp_secret')

        # Verify OTP
        if not OTP.verify_otp(otp=otp, otp_secret=otp_secret):
            raise forms.ValidationError("Invalid code, please try again.")
        return otp
    
class ConfirmPasswordForm(forms.Form):
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    recaptcha = forms.CharField(
        widget=forms.HiddenInput(),
        max_length=1024,
        required=False
    )

    def clean_recaptcha(self):
        cleaned_data = super(ConfirmPasswordForm, self).clean()
        recaptcha_response = cleaned_data.get('recaptcha')
        data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post(settings.RECAPTCHA_URL, data=data)
        result = r.json()

        if result.get('success') and result.get('score') > 0.5:
            # client is human
            pass
        else:
            raise forms.ValidationError('reCAPTCHA verification failed, please try again.')

    