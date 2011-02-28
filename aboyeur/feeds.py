from django.contrib.syndication.feeds import Feed
from aboyeur.models import Recipe

class RecentRecipes(Feed):
    title = "Conary Recipes: What's cooking today?"
    link = "/"
    description = "Latest Recipes published on Conary Recipes."

    def items(self):
        return Recipe.objects.filter(published=True).order_by('-date_posted')[:5]

    def item_link(self, item):
        return '/aboyeur/recipes/%d/' % item.id
