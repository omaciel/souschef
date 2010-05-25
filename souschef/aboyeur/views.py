from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.create_update import update_object
from aboyeur.models import *
from aboyeur.forms import *

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from djangoratings.views import AddRatingFromModel
from favorites.models import Favorite
from tagging.views import tagged_object_list
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

def front(request):
    recipes = Recipe.objects.filter(published=True).order_by('-date_updated')[:5]
    if recipes:
        featured_recipe = recipes[0]
    else:
        featured_recipe = []

    authors = []
    for user in User.objects.iterator():
        if user.has_perm('aboyeur.add_recipe'):
            user.recipe_count = Recipe.objects.filter(author=user).count()
            authors.append(user)
    authors.sort(key=lambda author: author.recipe_count, reverse=True)
    # Apply the syntax highligter
    html_formater = HtmlFormatter(linenos=True, style='native')
    if featured_recipe:
        featured_recipe.body = highlight(featured_recipe.body, PythonLexer(), html_formater)

    return render_to_response("front.html", {
        'extracss': html_formater.get_style_defs('.highlight'),
        'featured_recipe': featured_recipe,
        'languages': Category.objects.all(),
        'latest_recipes': recipes,
        'top_recipes': recipes,
        'top_sous_chefs': authors[:3]
    }, context_instance=RequestContext(request))

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
                published=True,
                tags__icontains=query
                )[:10]
    else:
        query = ""

    variables = RequestContext(request, {
        'form': form,
        'query': query,
        'recipes': recipes,
        'show_results': show_results,
        })

    if request.GET.has_key('ajax'):
        return render_to_response('recipe_list.html', variables)
    else:
        return render_to_response('recipes.html', variables)

def tagged_recipes(request, tag):
    queryset = Recipe.objects.all(published=True)
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

    try:
        recipe_stars = recipe.rating.score / recipe.rating.votes
    except ZeroDivisionError:
        recipe_stars = 0

    return render_to_response('aboyeur/recipe.html', {
        'extracss': html_formater.get_style_defs('.highlight'),
        'favorite_recipe': favorite_recipe,
        'next': reverse('recipe', args=[recipe.id]),
        'recipe': recipe,
        'recipe_stars': recipe_stars
    }, context_instance=RequestContext(request))

def _verify_permission(request, permission):
    if not request.user.has_perm(permission):
        response = render_to_response('403.html', context_instance=RequestContext(request))
        response.status_code = 403
        return response

@login_required
def add_recipe(request):
    _verify_permission(request, 'aboyeur.add_recipe')

    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return HttpResponseRedirect(reverse('profile_overview'))
    else:
        form = RecipeForm()

    return render_to_response('aboyeur/recipe_form.html', {
        'form': form
    }, context_instance=RequestContext(request))

@login_required
def delete_recipe(request, recipe_id):
    _verify_permission(request, 'aboyeur.delete_recipe')

    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == 'POST':
        for favorite in Favorite.objects.favorites_for_object(recipe):
            favorite.delete()

        recipe.delete()
        return HttpResponseRedirect(reverse('profile_overview'))
    else:
        return render_to_response('aboyeur/recipe_confirm_delete.html', {
            'recipe': recipe
        }, context_instance=RequestContext(request))

@login_required
def update_recipe(request, recipe_id):
    _verify_permission(request, 'aboyeur.change_recipe')

    return update_object(request,
        form_class=RecipeForm,
        object_id=recipe_id,
        post_save_redirect='/accounts/profile/',
        template_object_name='recipe'
    )

@login_required
def toggle_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    try:
        favorite = Favorite.objects.favorite_for_user(recipe, user=request.user)
        favorite.delete()
    except Favorite.DoesNotExist:
        Favorite.objects.create_favorite(recipe, request.user)
    return HttpResponseRedirect(reverse('recipe', args=[recipe.id]))

def add_rating(request, recipe_id, score):
    params = {
        'app_label': 'aboyeur',
        'model': 'recipe',
        'field_name': 'rating',
        'object_id': recipe_id,
        'score': score
    }

    response = AddRatingFromModel()(request, **params)

    if response.status_code == 200:
        return HttpResponseRedirect(reverse('recipe', args=[recipe_id]))
    return HttpResponseRedirect(reverse('recipe', args=[recipe_id]))
