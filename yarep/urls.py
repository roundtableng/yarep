from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fblogin/$', 'core.views.fblogin', name="fblogin"),
    url(r'^facebook/$', 'core.views.fbauthenticated', name="fbauth"),
    url(r'^twtlogin/$', 'core.views.twtlogin', name="twtlogin"),
    url(r'^twitter/$', 'core.views.twtauthenticated', name="twtauth"),
    url(r'^gplogin/$', 'core.views.gplogin', name='gplogin'),
    url(r'^gplus/$', 'core.views.gpauthenticated', name='gpauth'),
    #url(r'^profile/$', 'core.views.profile', name='profile'),
    url(r'^profile/$', 'tax.views.vat', name='profile'),
    #url(r'^profile/$', RedirectView.as_view(url=reverse_lazy('/tax/vat/'))),
    url(r'^replist/$', 'core.views.replist', name='replist'),
    url(r'^lga/$', 'core.views.select_lga', name='select_lga'),
    url(r'^get_lgas/$', 'core.views.get_lgas', name='get_lgas'),
    url(r'^$', 'core.views.home', name='home'),
    url(r'^register/$', 'core.views.registration', name='registration'),
    # url(r'^accounts/login/$',
    #    'django.contrib.auth.views.login',
    #    {'template_name': 'core/login.html'},
    #    name='login'),
    url(r'^accounts/login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'core/pages-login.html'},
        name='login'),
    url(r'^accounts/logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/accounts/login/'},
        name='logout'),
    url(r'^forum/', include('pybb.urls', namespace='pybb')),
    url(r'^newtopic/$', 'core.views.new_topic', name='new_topic'),
    url(r'^topic/(?P<topic_id>\d+)/$', 'core.views.topic', name='topic'),
    url(r'^tax/', include('tax.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
