from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(
        label = u'Enter a word to search for',
        widget = forms.TextInput(attrs={'size': 32})
    )
