from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from django.conf import settings
from userprofile.views import get_profiles
from aboyeur.views import *

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^souschef/', include('souschef.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Browsing
    url(r'^$', direct_to_template, {'extra_context': { 'profiles': get_profiles }, 'template': 'front.html' }),
    url(r'^accounts/', include('userprofile.urls')),
    url(r'^aboyeur/', include('aboyeur.urls.entries')),

    # Administration
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}
        ),
    )
