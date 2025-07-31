from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SignupEmailForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username")
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already registered.")
        return email


class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, label="Enter OTP")
