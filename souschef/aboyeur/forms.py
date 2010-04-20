from django import forms
from aboyeur.models import Recipe

class SearchForm(forms.Form):
    query = forms.CharField(
        label = u'Enter a word to search for',
        widget = forms.TextInput(attrs={'size': 32})
    )

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ('author', 'published')
