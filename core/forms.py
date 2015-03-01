from django import forms
from django.contrib.auth import authenticate


class RegistrationForm(forms.Form):
    email = forms.CharField(max_length=255)
    name = forms.CharField(max_length=255)
    pwd = forms.CharField(max_length=255)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=250)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def clean(self):
        if 'username' in self.cleaned_data and 'password' in self.cleaned_data:
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError(
                    'Please enter a valid username/password')
            if not user.is_active:
                raise forms.ValidationError(
                    'You are not allowed to login.\
                    Please contact the administrator')
            self.cleaned_data['user'] = user
            return self.cleaned_data
