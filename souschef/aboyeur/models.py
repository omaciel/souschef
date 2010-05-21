import datetime
import managers
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# External Modules
from djangoratings.fields import RatingField
from pygments import lexers
from tagging.fields import TagField
from tagging.models import Tag

class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(editable=False)
    language_code = models.CharField(max_length=50,
        help_text="This should be an alias of a Pygments lexer which can handle this language.")
    file_extension = models.CharField(max_length=10,
        help_text="The file extension to use when downloading recipes; leave out the dot.")
    mime_type = models.CharField(max_length=100,
        help_text="The HTTP Content-Type to use when downloading recipes.")

    objects = managers.RecipesManager()

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'categories'

    def save(self):
        if not self.id:
            self.slug = slugify(self.name)
        super(Category, self).save()

    def get_absolute_url(self):
        return ('cab.views.snippets.snippets_by_language', (), { 'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)

    def __unicode__(self):
        return self.name

    def get_lexer(self):
        """
        Returns an instance of the Pygments lexer for this language.
        """
        return lexers.get_lexer_by_name(self.language_code)

class Recipe(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=30)
    body = models.TextField()
    date_posted = models.DateField(editable=False)
    date_updated = models.DateTimeField(editable=False)
    published = models.BooleanField(default=False)

    rating = RatingField(range=5)
    category = models.ForeignKey(Category)
    tags = TagField()

    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self):
        return Tag.objects.get_for_object(self)

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
        # Use safe_mode in Markdown to prevent arbitrary tags.
        super(Recipe, self).save()

    def __unicode__(self):
        return self.title
