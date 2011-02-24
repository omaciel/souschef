from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from django.conf import settings
from aboyeur.views import *
from souschef import aboyeur

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^souschef/', include('souschef.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Browsing
    url(r'^$', front, name="frontpage"),
    url(r'^contact', 'aboyeur.views.show_contact', name="contact"),
    (r'^tag/(?P<tag_id>\d+)', 'aboyeur.views.tagged_recipes'),
    url(r'^accounts/', include('demoprofile.urls')),
    url(r'^accounts/', include('userprofile.urls')),
    url(r'^aboyeur/', include('aboyeur.urls.entries')),
    url(r'^comments/', include('django.contrib.comments.urls')),

    # Administration
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}
        ),
    )
