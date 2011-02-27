from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.shortcuts import render_to_response
from django.template import RequestContext
from aboyeur.forms import RecipeForm
from aboyeur.models import *
from favorites.models import Favorite
from userprofile.models import EmailValidation, Avatar
from userprofile.forms import RegistrationForm
from django.contrib.auth.models import User, SiteProfileNotAvailable
from django.http import HttpResponseRedirect

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
        'validated': validated,
    }
    return render_to_response(template, data, context_instance=RequestContext(request))

def register(request):

    invitation = False

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            if 'invitation' in request.session:
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                newuser = User.objects.create_user(username=username, email='', password=password)
                # Retrieve the invitation object.
                invitation = Invitation.objects.get(
                    id=request.session['invitation']
                    )

                if form.cleaned_data.get('email'):
                    newuser.email = form.cleaned_data.get('email')
                    EmailValidation.objects.add(user=newuser, email=newuser.email)

                newuser.save()
                # Delete the invitation from the database and session.
                invitation.delete()
                del request.session['invitation']
                return HttpResponseRedirect('%scomplete/' % request.path_info)
            else:
                raise SiteProfileNotAvailable
    else:
        form = RegistrationForm()

    template = "userprofile/account/registration.html"
    data = { 'form': form}
    return render_to_response(template, data, context_instance=RequestContext(request))
