from django.conf.urls import url


urlpatterns = [
    url(r'companyreg/$', 'tax.views.company_reg', name='company_reg'),
    url(r'vat/$', 'tax.views.vat', name='vat'),
    url(r'history/$', 'tax.views.history', name='history'),
    url(r'payment/$', 'tax.views.payment', name='payment'),
    ]
