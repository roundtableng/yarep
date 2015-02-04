from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

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
    url(r'^profile/$', 'core.views.profile', name='profile'),
    url(r'^lga/$', 'core.views.select_lga', name='select_lga'),
    url(r'^get_lgas/$', 'core.views.get_lgas', name='get_lgas'),
    url(r'^$', TemplateView.as_view(
        template_name='core/home.html'), name="home"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
