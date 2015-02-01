from django import forms


class RegistrationForm(forms.Form):
    email = forms.CharField(max_length=255)
    name = forms.CharField(max_length=255)
