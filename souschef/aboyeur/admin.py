from django.contrib import admin
from favorites.models import Favorite
from souschef.aboyeur.models import Category, Recipe

class RecipeInline(admin.StackedInline):
    model = Recipe

class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        RecipeInline,
    ]
admin.site.register(Category, CategoryAdmin)

class FavoriteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Favorite, FavoriteAdmin)

class RecipeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Recipe, RecipeAdmin)