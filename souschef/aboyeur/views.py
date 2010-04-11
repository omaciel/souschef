# Create your views here.
from aboyeur.models import Recipe
from tagging.views import tagged_object_list

def tagged_recipes(request, tag):
    queryset = Recipe.objects.all()
    return tagged_object_list(request, queryset, tag, paginate_by=25,
        allow_empty=True, template_object_name='recipe')
