from django.forms import ModelForm, PasswordInput
from helper_app.models import Accounts, Skills
from django.contrib.auth.models import User as Usermodel

class UserForm(ModelForm):
    class Meta:
        model = Accounts
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
