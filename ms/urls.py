from django.conf import settings
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'hackathon.views.index', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/', 'hackathon.views.test', name='test'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^turn/(?P<id>[^\.]+)', 'hackathon.views.get_turn_data', name='get_turn'),
)
