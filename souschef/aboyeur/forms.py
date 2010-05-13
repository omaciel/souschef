from django import forms
from tinymce.widgets import TinyMCE
from aboyeur.models import Recipe

class SearchForm(forms.Form):
    query = forms.CharField(
        label = u'Enter a word to search for',
        widget = forms.TextInput(attrs={'size': 32})
    )

class RecipeForm(forms.ModelForm):
    body = forms.CharField(widget=TinyMCE(attrs={'cols': 8, 'rows': 10}))

    class Meta:
        model = Recipe
        exclude = ('author',)
