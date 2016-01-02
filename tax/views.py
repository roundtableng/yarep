from django.shortcuts import render


def company_reg(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'tax/company_registration.html', {})
