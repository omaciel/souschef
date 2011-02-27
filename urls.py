from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from django.conf import settings
from aboyeur.views import *
from souschef import aboyeur

admin.autodiscover()

urlpatterns = patterns('',

    # Browsing
    url(r'^$', front, name="frontpage"),
    url(r'^contact', 'aboyeur.views.show_contact', name="contact"),
    url(r'^user_map', 'aboyeur.views.show_user_map', name="user_map"),
    (r'^tag/(?P<tag_id>\d+)', 'aboyeur.views.tagged_recipes'),
    url(r'^accounts/profile/edit/personal/$', 'aboyeur.django_profile_overrides.personal', name='profile_edit_personal'),
    url(r'^accounts/profile/$', 'aboyeur.django_profile_overrides.overview', name='profile_overview'),
    url(r'^accounts/', include('demoprofile.urls')),
    url(r'^accounts/', include('userprofile.urls')),
    url(r'^aboyeur/', include('aboyeur.urls.entries')),
    url(r'^comments/', include('django.contrib.comments.urls')),

    (r'^friend/invite/$', friend_invite),
    (r'^friend/accept/(\w+)/$', friend_accept),

    # Administration
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}
        ),
    )
