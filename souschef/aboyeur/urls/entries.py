from django.conf.urls.defaults import *
from aboyeur.views import *

urlpatterns = patterns('',

    # Browsing
    (r'^$', recipes_page),
)
