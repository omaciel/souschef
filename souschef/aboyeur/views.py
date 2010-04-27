from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from aboyeur.models import *
from aboyeur.forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from favorites.models import Favorite
from tagging.views import tagged_object_list
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

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

def recipes(request, id):
    recipe = get_object_or_404(Recipe, id=id)

    # Apply the syntax highligter
    html_formater = HtmlFormatter(linenos=True, style='native')
    recipe.body = highlight(recipe.body, PythonLexer(), html_formater)
    
    # Verify if its a favorite recipe for the current user
    try:
        Favorite.objects.favorite_for_user(recipe, user=request.user)
        favorite_recipe = True
    except Favorite.DoesNotExist:
        favorite_recipe = False

    return render_to_response('aboyeur/recipe.html', {
        'extracss': html_formater.get_style_defs('.highlight'),
        'favorite_recipe': favorite_recipe,
        'recipe': recipe,
    }, context_instance=RequestContext(request))

@login_required
def add_recipe(request):
    if not request.user.has_perm('aboyeur.add_recipe'):
        response = render_to_response('403.html', context_instance=RequestContext(request))
        response.status_code = 403
        return response
    
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        print form.data
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            # TODO: redirect to the author's recipes
            return HttpResponseRedirect('/recipes/')
    else:
        form = RecipeForm()
    return render_to_response('aboyeur/add_recipe.html', {
        'form': form
    }, context_instance=RequestContext(request))

@login_required
def toggle_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    try:
        favorite = Favorite.objects.favorite_for_user(recipe, user=request.user)
        favorite.delete()
    except Favorite.DoesNotExist:
        Favorite.objects.create_favorite(recipe, request.user)
    return HttpResponseRedirect(reverse('recipe', args=[recipe.id]))