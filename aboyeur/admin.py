from django.contrib import admin
from favorites.models import Favorite
from souschef.aboyeur.models import Recipe

class FavoriteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Favorite, FavoriteAdmin)

class RecipeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Recipe, RecipeAdmin)
