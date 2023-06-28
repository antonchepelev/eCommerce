from django import forms
from .models import Accounts


class CreateAccountForm(forms.ModelForm):
    class Meta:
        model = Accounts
        fields = "__all__"


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class EmailVerificationForm(forms.Form):
    confirmation_number = forms.CharField(max_length=10)


