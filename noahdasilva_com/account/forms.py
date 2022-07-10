from django.contrib.auth import get_user_model
from django import forms


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password',]


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
