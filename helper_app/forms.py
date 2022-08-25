from django.forms import ModelForm, PasswordInput
from helper_app.models import Skills
from django.contrib.auth.models import User as Usermodel
from django import forms

class UserForm(ModelForm):
    class Meta:
        model = Usermodel
        fields = ('username', 'password')
        widgets = {
            'password': PasswordInput(),
        }

class RegisterForm(ModelForm):
    class Meta:
        model = Usermodel
        fields = ('username', 'password', 'email')
        widgets = {
            'password': PasswordInput(),
        }
