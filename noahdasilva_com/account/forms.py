from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth import forms as auth_forms
import re


class SignUpForm(forms.ModelForm):
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password',]

    MIN_LENGTH = 8
    def clean_password(self):
        password = self.cleaned_data.get('password')

        # At least 8 characters long
        if len(password) < self.MIN_LENGTH:
            raise forms.ValidationError("Password must be at least %d characters long." % self.MIN_LENGTH)
        
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
                "The new password must contain at least one letter, number," \
                " and special character.")

        # ... any other validation you want ...

        return password


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'full_name', 'email',]


class CustomSetPasswordForm(auth_forms.SetPasswordForm):
    MIN_LENGTH = 8
    def clean_new_password2(self):
        password = self.cleaned_data.get('new_password2')
        first_password = self.cleaned_data.get('new_password1')

        # Passwords must match
        if password != first_password:
            raise forms.ValidationError("Passwords do not match.")
        
        # At least 8 characters long
        if len(password) < self.MIN_LENGTH:
            raise auth_forms.ValidationError("Password must be at least %d characters long." % self.MIN_LENGTH)
        
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
                "The new password must contain at least one letter, number," \
                " and special character.")

        # ... any other validation you want ...

        return password


class CustomPasswordChangeForm(auth_forms.PasswordChangeForm):
    MIN_LENGTH = 8
    def clean_new_password2(self):
        password = self.cleaned_data.get('new_password2')
        old_password = self.cleaned_data.get('old_password')

        # Must be new password
        if password == old_password:
            raise auth_forms.ValidationError("New password must be different from old password.")

        # At least 8 characters long
        if len(password) < self.MIN_LENGTH:
            raise auth_forms.ValidationError("Password must be at least %d characters long." % self.MIN_LENGTH)
        
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
                "The new password must contain at least one letter, number," \
                " and special character.")

        # ... any other validation you want ...

        return password