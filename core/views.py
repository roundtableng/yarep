from django.http import HttpResponse
from django.contrib.auth.models import User

from core.forms import RegistrationForm


def fblogin(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            User.objects.create_user(name, email)
            return HttpResponse('Ok')
    return HttpResponse('Bad')
