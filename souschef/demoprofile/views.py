from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.shortcuts import render_to_response
from django.template import RequestContext
from aboyeur.forms import RecipeForm
from aboyeur.models import Recipe
from favorites.models import Favorite
from userprofile.models import EmailValidation, Avatar

if not settings.AUTH_PROFILE_MODULE:
    raise SiteProfileNotAvailable
try:
    app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
    Profile = models.get_model(app_label, model_name)
except (ImportError, ImproperlyConfigured):
    raise SiteProfileNotAvailable

if not Profile:
    raise SiteProfileNotAvailable

@login_required
def overview(request):
    """
    Main profile page
    """
    profile, created = Profile.objects.get_or_create(user=request.user)
    validated = False
    try:
        email = EmailValidation.objects.get(user=request.user).email
    except EmailValidation.DoesNotExist:
        email = request.user.email
        if email: validated = True
    
    favorites = Favorite.objects.favorites_for_model(Recipe, user=request.user)
    user_recipes = Recipe.objects.filter(author=request.user)
    
    template = "userprofile/profile/overview.html"
    data = {
        'section': 'overview',
        'email': email,
        'favorites': favorites,
        'form': RecipeForm(),
        'user_recipes': user_recipes,
        'validated': validated
    }
    return render_to_response(template, data, context_instance=RequestContext(request))
