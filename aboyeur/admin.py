from django.contrib import admin
from favorites.models import Favorite
from souschef.aboyeur.models import Invitation, Recipe

class FavoriteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Favorite, FavoriteAdmin)

class RecipeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Recipe, RecipeAdmin)

class InvitationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Invitation, InvitationAdmin)
