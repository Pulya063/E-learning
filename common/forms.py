from django import forms
from django.contrib.auth.models import User


class UserRegister(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']



class UserLogin(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserUpdateForm(UserRegister):
    pass