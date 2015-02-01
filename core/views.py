from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login

from core.forms import RegistrationForm


def fblogin(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            try:
                user = User.objects.get(username=email)
            except User.DoesNotExist:
                user = User.objects.create_user(email, email)
                user.first_name = name
                user.save()
            login(request, user)
            return HttpResponse('Ok')
    return HttpResponse('Bad')
