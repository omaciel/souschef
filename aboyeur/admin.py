from django.contrib import admin
from souschef.aboyeur.models import Category, Recipe

class RecipeInline(admin.StackedInline):
    model = Recipe

class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        RecipeInline,
    ]

admin.site.register(Category, CategoryAdmin)
