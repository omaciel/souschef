import datetime
import managers
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# External Modules
from djangoratings.fields import RatingField
from tagging.fields import TagField
from tagging.models import Tag

class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(editable=False)

    objects = managers.RecipesManager()

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'categories'

    def save(self):
        if not self.id:
            self.slug = slugify(self.name)
        super(Category, self).save()

    def __unicode__(self):
        return self.name

class Recipe(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=30)
    body = models.TextField()
    label = models.CharField(max_length=100, blank=True, null=True)
    date_posted = models.DateField(editable=False, blank=True, null=True)
    date_updated = models.DateTimeField(editable=False, blank=True, null=True)
    published = models.BooleanField(default=False)

    rating = RatingField(range=5)
    category = models.ForeignKey(Category)
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
            'fields': ('title', 'category', 'author', 'tags', )}),
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
