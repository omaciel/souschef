from django.conf.urls.defaults import *
from demoprofile.views import *

urlpatterns = patterns('',
    url(r'^profile/$', overview, name='profile_overview'),
)