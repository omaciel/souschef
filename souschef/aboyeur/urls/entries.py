from django.conf.urls.defaults import *
from aboyeur.views import *

urlpatterns = patterns('',

    # Browsing
    url(r'^$', recipes_page, name='recipes'),
    url(r'^recipes/(?P<id>\d+)/$', recipes, name='recipe'),
    url(r'^recipes/add/$', add_recipe, name='add_recipe'),
    url(r'^recipes/toggle_favorite/(?P<recipe_id>\d+)/$', toggle_favorite, name='toggle_favorite'),
)
