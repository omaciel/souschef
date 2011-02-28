from django.conf.urls.defaults import *
from souschef.aboyeur.feeds import *
from souschef.aboyeur.views import *

feeds = {
    'recent': RecentRecipes,
    'user': UserRecipes,
}

urlpatterns = patterns('',

    # Browsing
    url(r'^$', recipes_page, name='recipes'),
    url(r'^recipes/(?P<id>\d+)/$', recipes, name='recipe'),
    url(r'^recipes/add/$', add_recipe, name='add_recipe'),
    url(r'^recipes/edit/(?P<recipe_id>\d+)/$', update_recipe, name='edit_recipe'),
    url(r'^recipes/delete/(?P<recipe_id>\d+)/$', delete_recipe, name='delete_recipe'),
    url(r'^recipes/toggle_favorite/(?P<recipe_id>\d+)/$', toggle_favorite, name='toggle_favorite'),
    url(r'^recipes/rate/(?P<recipe_id>\d+)/(?P<score>\d+)/', add_rating, name='add_rating'),
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)
