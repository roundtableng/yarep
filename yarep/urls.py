from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fblogin/$', 'core.views.fblogin', name="fblogin"),
    url(r'^twtlogin/$', 'core.views.twtlogin', name="twtlogin"),
    url(r'^twitter/$', 'core.views.twtauthenticated', name="twtauth"),
    url(r'^profile/$', TemplateView.as_view(
        template_name='core/profile.html'), name="profile"),
    url(r'^$', TemplateView.as_view(
        template_name='core/home.html'), name="home"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
