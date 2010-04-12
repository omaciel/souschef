from django.template import RequestContext
from django.shortcuts import render_to_response

from aboyeur.models import *
from aboyeur.forms import *
from tagging.views import tagged_object_list

def recipes_page(request):
    form = SearchForm()
    recipes = []
    show_results = []

    if 'query' in request.GET:
        show_results = True
        query = request.GET['query'].strip()
        if query:
            form = SearchForm({'query' : query})
            recipes = Recipe.objects.filter(
                tags__icontains=query
                )[:10]

    variables = RequestContext(request, {
        'form': form,
        'recipes': recipes,
        'show_results': show_results,
        })

    if request.GET.has_key('ajax'):
        return render_to_response('recipe_list.html', variables)
    else:
        return render_to_response('recipes.html', variables)

def tagged_recipes(request, tag):
    queryset = Recipe.objects.all()
    return tagged_object_list(request, queryset, tag, paginate_by=25,
        allow_empty=True, template_object_name='recipe')
