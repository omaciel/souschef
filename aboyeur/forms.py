#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

from django import forms
from aboyeur.models import Recipe, Recipe_file

class SearchForm(forms.Form):
    query = forms.CharField(
        label = u'Enter a word to search for',
        widget = forms.TextInput(attrs={'size': 32})
    )

class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        exclude = ('author',)

class Recipe_File_Form(forms.ModelForm):
    class Meta:
        model = Recipe_file
        exclude = ('recipe')

class FriendInviteForm(forms.Form):
    name = forms.CharField(label = 'Friend\'s Name')
    email = forms.EmailField(label = 'Friend\'s Email')
