from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from core.forms import RegistrationForm


def fblogin(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            pwd = form.cleaned_data['pwd']
            try:
                user = User.objects.get(username=email, password=pwd)
            except User.DoesNotExist:
                user = User.objects.create_user(email, email)
                user.first_name = name
                user.save()
            usr = authenticate(username=email, password=pwd)
            login(request, usr)
            return HttpResponse('Ok')
    return HttpResponse('Bad')
