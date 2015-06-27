from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=250)
    email = forms.CharField(max_length=250)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    pwd2 = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def clean_email(self):
        if 'email' in self.cleaned_data:
            if User.objects.filter(email=self.cleaned_data['email']):
                raise forms.ValidationError('This email is already in use')
            return self.cleaned_data['email']

    def clean(self):
        if 'password' in self.cleaned_data and 'pwd2' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['pwd2']:
                raise forms.ValidationError("The passwords don't match")
            return self.cleaned_data


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


class TopicForm(forms.Form):
    name = forms.CharField(max_length=100)
    post = forms.CharField(widget=forms.Textarea, max_length=200)


class PostForm(forms.Form):
    post = forms.CharField(widget=forms.Textarea(attrs={'rows': '5'}), max_length=200)
