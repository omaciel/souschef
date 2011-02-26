import datetime
from django.db import models
from django.contrib.auth.models import User
import os.path

# External Modules
from djangoratings.fields import RatingField
from tagging.fields import TagField
from tagging.models import Tag
from django import forms
from django.core.exceptions import ValidationError

def get_recipe_files_path(instance, filename):
    return os.path.join('recipe_files', str(instance.recipe.id), filename)

class Recipe(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=30)
    body = models.TextField()
    install_path = models.CharField(max_length=150, blank=True, null=True)
    url = models.URLField(max_length=250, blank=True, null=True)
    date_posted = models.DateField(editable=False, blank=True, null=True)
    date_updated = models.DateTimeField(editable=False, blank=True, null=True)
    published = models.BooleanField(default=False)

    rating = RatingField(range=5)
    tags = TagField()

    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def stars(self):
        return range(self.rating_score)

    class Meta:
        ordering = ('-date_updated',)

    class Admin:
        fields = (
            ('Metadata', {
            'fields': ('title', 'author', 'tags', )}),
            ('None', {
             'fields': ('body')}),
            )

    def save(self):
        if not self.id:
            self.date_updated = datetime.datetime.now()
        if self.published:
            self.date_posted = datetime.datetime.now()
        super(Recipe, self).save()

    def __unicode__(self):
        return self.title
    
class Recipe_file(models.Model):
    recipe = models.ForeignKey(Recipe)
    file = models.FileField(upload_to=get_recipe_files_path)

    def filename(self):
        return os.path.basename(self.file.name)
    
    def clean(self):
        if not self.file.name.split('.')[-1] in ['zip', 'tar', 'gz', 'bz2']:
            raise ValidationError("Unsupported extension")
        if self.file.size > 500*1024:
            raise ValidationError("File size over limit")
    
