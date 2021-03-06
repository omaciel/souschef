from aboyeur.models import Invitation
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.views.generic.create_update import update_object
from aboyeur.models import *
from aboyeur.forms import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from djangoratings.views import AddRatingFromModel
from favorites.models import Favorite
from tagging.views import tagged_object_list
from tagging.models import Tag
from tagging.models import TaggedItem
import random
from django.core.paginator import Paginator
import smtplib
from django.contrib.auth.models import User
from decimal import *
try:
    import json
except ImportError:
    import simplejson as json
from django.http import HttpResponse
from urllib2 import urlopen
from xml.etree import ElementTree
import StringIO
import gzip
from django.contrib import messages

def front(request):
    recipes = Recipe.objects.filter(published=True).order_by('-date_updated')[:5]
    top_recipes = Recipe.objects.filter(published=True).order_by('-rating_score')[:5]
    if recipes:
        featured_recipe = top_recipes[random.randint(0,len(top_recipes) - 1)]
        try:
            featured_recipe.stars = featured_recipe.rating.score / featured_recipe.rating.votes
        except ZeroDivisionError:
            featured_recipe.stars = 0
    else:
        featured_recipe = []

    authors = []
    for user in User.objects.iterator():
        if user.has_perm('aboyeur.add_recipe'):
            user.recipe_count = Recipe.objects.filter(author=user, published=True).count()
            if user.recipe_count > 0:
                authors.append(user)
    authors.sort(key=lambda author: author.recipe_count, reverse=True)
    tagcloud = []
    tag_count = TaggedItem.objects.all().count()
    for tag in Tag.objects.all():
        tagcloud.append([tag, float(TaggedItem.objects.filter(tag__exact = tag).count())/ tag_count * 200 + 100, tag.id])
    tagcloud.sort(key=lambda tag: tag[1], reverse=True)
    tagcloud = tagcloud[:10]
    return render_to_response("front.html", {
        'featured_recipe': featured_recipe,
        'latest_recipes': recipes,
        'top_recipes': top_recipes,
        'top_sous_chefs': authors[:3],
        'tagcloud': tagcloud
    }, context_instance=RequestContext(request))

def recipes_page(request):
    form = SearchForm()
    recipes = []
    show_results = []

    if 'query' in request.GET:
        show_results = True
        query = request.GET['query'].strip()
        if query:
            recipes = Recipe.objects.filter(Q(title__icontains = query) | Q(body__icontains = query) | Q(tags__icontains = query), Q(published__exact=True))[:10]
            messages.add_message(request, messages.SUCCESS, 'Search complete')
    else:
        query = ""

    paginator = Paginator(recipes,5)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    recipes = paginator.page(page)



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

def tagged_recipes(request, tag_id):
    form = SearchForm()
    tag = Tag.objects.get(pk=tag_id)
    queryset = TaggedItem.objects.get_by_model(Recipe, tag)

    paginator = Paginator(queryset,5)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    queryset = paginator.page(page)


    variables = RequestContext(request, {
        'recipes': queryset,
        'form': form,
        'tag': tag
        })

    return render_to_response('recipes.html', variables)

def recipes(request, id):
    recipe = get_object_or_404(Recipe, id=id)

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
    file_form = Recipe_File_Form()
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            if request.FILES:
                recipe_file = request.FILES['file']
                recipe_file_container = Recipe_file()
                recipe_file_container.file = recipe_file
                try:
                    recipe_file_container.clean()
                except:
                    return render_to_response('userprofile/profile/overview.html', {
                        'form': form, 'recipe':recipe, 'file_error': 'Attachment does not comply with limits', 'file_form':file_form
                    }, context_instance=RequestContext(request))
                recipe.save()
                recipe_file_container.recipe = recipe
                recipe.recipe_file_set.all().delete()
                recipe_file_container.save()
            else:
                recipe.save()
            messages.add_message(request, messages.SUCCESS, 'Recipe created')

            return HttpResponseRedirect(reverse('profile_overview'))
        else:
            messages.add_message(request, messages.ERROR, 'Recipe form is not valid')
    else:
        form = RecipeForm()

    return render_to_response('aboyeur/recipe_form.html', {
        'form': form
    }, context_instance=RequestContext(request))

@login_required
def delete_recipe(request, recipe_id):
    _verify_permission(request, 'aboyeur.delete_recipe')

    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.author != request.user:
        return redirect('/')

    if request.method == 'POST':
        for favorite in Favorite.objects.favorites_for_object(recipe):
            favorite.delete()

        recipe.delete()
        messages.add_message(request, messages.SUCCESS, 'Recipe deleted')
        return HttpResponseRedirect(reverse('profile_overview'))
    else:
        return render_to_response('aboyeur/recipe_confirm_delete.html', {
            'recipe': recipe
        }, context_instance=RequestContext(request))

@login_required
def update_recipe(request, recipe_id):
    file_form = Recipe_File_Form()
    _verify_permission(request, 'aboyeur.change_recipe')
    recipe = Recipe.objects.get(pk=recipe_id)
    if recipe.author != request.user:
        return redirect('/')
    form = RecipeForm(request.POST)
    if request.FILES:
        recipe_file = request.FILES['file']
        recipe_file_container = Recipe_file()
        recipe_file_container.recipe = recipe
        recipe_file_container.file = recipe_file
        try:
            recipe_file_container.clean()
        except:
            return render_to_response('aboyeur/recipe_form.html', {
                'form': form, 'file_form':file_form, 'recipe':recipe, 'file_error': 'Attachment does not comply with limits'
            }, context_instance=RequestContext(request))
            
        recipe.recipe_file_set.all().delete()
        recipe_file_container.save()

    return update_object(request,
        form_class=RecipeForm,
        object_id=recipe_id,
        post_save_redirect='/accounts/profile/',
        template_object_name='recipe',
        extra_context={'file_form':file_form}
    )

@login_required
def toggle_favorite(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    try:
        favorite = Favorite.objects.favorite_for_user(recipe, user=request.user)
        favorite.delete()
    except Favorite.DoesNotExist:
        Favorite.objects.create_favorite(recipe, request.user)
    messages.add_message(request, messages.SUCCESS, 'Recipe set as favourite')
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
    messages.add_message(request, messages.SUCCESS, 'Recipe rated')
    return HttpResponseRedirect(reverse('recipe', args=[recipe_id]))

def show_contact(request):
    return render_to_response('contact.html', context_instance=RequestContext(request))

def show_user_map(request):
    users = User.objects.all()
    profiles = []
    for user in users:
        try:
            profile = user.get_profile()
            if profile.latitude and profile.longitude:
                random_add = Decimal(str(random.uniform(-0.009,0.009))).quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)
                profile.latitude = profile.latitude + random_add
                profile.longitude = profile.longitude + random_add
                profiles.append(profile)
        except:
            pass
    return render_to_response('user_map.html', {'profiles':profiles},context_instance=RequestContext(request))

@login_required
def friend_invite(request):
    if request.user.is_staff == False:
        return redirect('/accounts/profile')
    if request.method == 'POST':
        form = FriendInviteForm(request.POST)
        random_password = User.objects.make_random_password(20)
        while Invitation.objects.filter(code__exact = random_password).count() > 0:
            random_password = User.objects.make_random_password(20)
        if form.is_valid():
            invitation = Invitation(
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    code=random_password,
                    active=True,
                    sender=request.user
                    )
            invitation.save()
            try:
                invitation.send()
                request.user.message_set.create(
                        message=u'An invitation was sent to %s.' %
                        invitation.email
                        )
            except smtplib.SMTPException:
                request.user.message_set.create(
                        message=u'An error happened when '
                        u'sending the invitation.')
            messages.add_message(request, messages.SUCCESS, 'Invitation sent')
            return HttpResponseRedirect('/friend/invite/')
        else:
            messages.add_message(request, messages.ERROR, 'Invitation not sent')
            return HttpResponseRedirect('/friend/invite/')
    else:
        form = FriendInviteForm()
        variables = {'form': form}
    return render_to_response('friend_invite.html', variables,context_instance=RequestContext(request))

def friend_accept(request, code):
    invitation = get_object_or_404(Invitation, code__exact=code)
    request.session['invitation'] = invitation.id
    return HttpResponseRedirect('/accounts/register/')

def tags_service(request):
    try:
        query = request.GET['term']
        query = query.split(',')[-1].strip()
        tags = Tag.objects.filter(name__icontains = query)[:10]
    except:
        tags = Tag.objects.all()[:10]
    tag_array = []
    for tag in tags:
        tag_array.append(tag.name)
    json_data = json.dumps(tag_array)
    return HttpResponse(json_data,content_type='application/json')

def recipe_sync(request):
    try:
        build_label = request.POST['build_label']
        #Info
        repository_path = 'foresight.rpath.org@' + build_label.split('@')[-1]
        if build_label.index('='):
            package_name = build_label.split('=')[0]
        else:
            package_name = build_label.split('@')[0]

        #Get the repository source path
        repository_list = urlopen('https://www.rpath.org/repos/foresight/api').read()
        repository_parsed = ElementTree.XML(repository_list)
        for repository in repository_parsed.getiterator('label'):
            if repository.find('name').text == repository_path:
                source_path = repository.getiterator('sources')[0].attrib['href'].strip()
        #Get the trove info
        source_list = urlopen(source_path).read()
        source_parsed = ElementTree.XML(source_list)
        for source in source_parsed.getiterator('node'):
            if source.find('name').text == package_name+':source':
                trove_path = source.getiterator('trovelist')[0].attrib['id']
        #Get the recipe info
        trove_list = urlopen(trove_path).read()
        trove_parsed = ElementTree.XML(trove_list)
        for trove in trove_parsed.getiterator('fileref'):
            trove_name = '/' + package_name+'.recipe'
            if trove.find('path').text == trove_name:
                recipe_path = trove.getiterator('inode')[0].attrib['id']
                #Get the recipe file
        recipe_list = urlopen(recipe_path).read()
        recipe_parsed = ElementTree.XML(recipe_list)
        for recipe in recipe_parsed.getiterator('file'):
            recipe_file = recipe.getiterator('content')[0].attrib['href']
        recipe_content = urlopen(recipe_file).read()
        stream = StringIO.StringIO(recipe_content)
        zipper = gzip.GzipFile(fileobj=stream)
        recipe_text = zipper.read()
        return HttpResponse(recipe_text)
    except:
        return HttpResponse('Error')

