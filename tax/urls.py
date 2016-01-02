from django.conf.urls import url


urlpatterns = [
    url(r'companyreg/$', 'tax.views.company_reg', name='company_reg'),
    ]
