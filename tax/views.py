from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def company_reg(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'tax/company_registration.html', {})


def vat(request):
    return render(request, 'tax/vat.html', {})


def history(request):
    return render(request, 'tax/history.html', {})


def payment(request):
    return render(request, 'tax/payment.html', {})


def dashboard(request):
    return render(request, 'tax/dash.html', {})
