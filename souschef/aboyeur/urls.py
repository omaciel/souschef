from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib.auth.decorators import login_required
from tagging.views import tagged_object_list
from souschef.aboyeur.models import Recipe

urlpatterns = patterns('',
    url(r'^recipe/tag/(?P<tag>[^/]+)/$',
        tagged_object_list,
        dict(queryset_or_model=Recipe, paginate_by=10, allow_empty=True,
             template_object_name='recipe'),
        name='recipe_tag_detail'),
)
