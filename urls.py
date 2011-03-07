from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from django.conf import settings
from aboyeur.views import *
from souschef import aboyeur
from diario.feeds.entries import RssEntriesFeed, AtomEntriesFeed
from diario.feeds.tagged import RssEntriesByTagFeed, AtomEntriesByTagFeed

# Overriding 500 error handler
handler500 = 'souschef.views.server_500_error'
handler404 = 'souschef.views.server_404_error'

admin.autodiscover()

entries_feeds = {
    'rss': RssEntriesFeed,
    'atom': AtomEntriesFeed,
}

entries_by_tag_feeds = {
    'rss': RssEntriesByTagFeed,
    'atom': AtomEntriesByTagFeed,
}

urlpatterns = patterns('',

    # Browsing
    url(r'^$', front, name="frontpage"),
    url(r'^contact', 'aboyeur.views.show_contact', name="contact"),
    url(r'^user_map', 'aboyeur.views.show_user_map', name="user_map"),
    (r'^tag/(?P<tag_id>\d+)', 'aboyeur.views.tagged_recipes'),
    url(r'^tags_service/', 'aboyeur.views.tags_service', name="tags_service"),
    url(r'^accounts/profile/edit/personal/$', 'aboyeur.django_profile_overrides.personal', name='profile_edit_personal'),
    url(r'^accounts/profile/$', 'aboyeur.django_profile_overrides.overview', name='profile_overview'),
    url(r'^accounts/register/$', 'aboyeur.django_profile_overrides.register', name='profile_register'),
    url(r'^accounts/', include('demoprofile.urls')),
    url(r'^accounts/', include('userprofile.urls')),
    url(r'^aboyeur/', include('aboyeur.urls.entries')),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^recipe_sync/', 'aboyeur.views.recipe_sync', name="recipe_sync"),

    (r'^friend/invite/$', friend_invite),
    (r'^friend/accept/(\w+)/$', friend_accept),

    # weblog
    url(r'^blog/', include('diario.urls.entries')),
    url(r'^blog/(?P<slug>(rss|atom))/$', 'diario.views.syndication.feed', {'feed_dict': entries_feeds}),

    # Administration
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^500/$', 'souschef.views.server_500_error'),
        url(r'^404/$', 'souschef.views.server_404_error'),
        url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}
        ),
    )
