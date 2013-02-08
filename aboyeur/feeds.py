from django.contrib.syndication.views import Feed
from aboyeur.models import Recipe
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class RecentRecipes(Feed):
    title = "Conary Recipes: What's cooking today?"
    link = "/"
    description = "Latest Recipes published on Conary Recipes."

    def items(self):
        return Recipe.objects.filter(published=True).order_by('-date_posted')[:5]

    def item_link(self, item):
        return '/aboyeur/recipes/%d/' % item.id

class UserRecipes(Feed):
    def get_object(self, request, username):
        return get_object_or_404(User, username=username)
    def title(self, user):
        return (
                u'Conary Recipes | Recipes by Chef %s' % user.username
                )
    def link(self, user):
        return '/feeds/user/%s/' % user.username

    def description(self, user):
        return u'Recent recipes posted by Chef %s' % user.username

    def items(self, user):
        return user.recipe_set.order_by('-id')[:10]
