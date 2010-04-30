from django.contrib.auth.models import User
from django.db import models
from djangoratings.fields import RatingField
from tagging.fields import TagField
from tagging.models import Tag

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

class Recipe(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=30)
    body = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    published = models.BooleanField(default=False)

    rating = RatingField(range=5)
    category = models.ForeignKey(Category)
    tags = TagField()

    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self):
        return Tag.objects.get_for_object(self)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('title',)
