from django import forms
from tinymce.widgets import TinyMCE
from aboyeur.models import Recipe

class SearchForm(forms.Form):
    query = forms.CharField(
        label = u'Enter a word to search for',
        widget = forms.TextInput(attrs={'size': 32})
    )

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ('author',)
        widgets = {
            'body': forms.CharField(widget = TinyMCE(
                attrs={
                    'cols': 80,
                    'rows': 30
                }
            ))
        }
