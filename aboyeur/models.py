import datetime
from django.db import models
from django.contrib.auth.models import User
import os.path

# External Modules
from djangoratings.fields import RatingField
from tagging.fields import TagField
from tagging.models import Tag
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context
from django.conf import settings

def get_recipe_files_path(instance, filename):
    return os.path.join('recipe_files', str(instance.recipe.id), filename)

class Recipe(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=30)
    body = models.TextField()
    install_path = models.CharField("Build Label", max_length=150, blank=True, null=True, help_text="You can install this package in your system by using this label.")
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

class Invitation(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    code = models.CharField(max_length=20)
    active = models.BooleanField()
    sender = models.ForeignKey(User)

    def __unicode__(self):
        return u'%s, %s' % (self.sender.username, self.email)

    def send(self):
        subject = u'Invitation to join Conary Recipes'
        link = 'http://%s/friend/accept/%s/' % (
                settings.SITE_HOST,
                self.code
                )
        template = get_template('invitation_email.txt')
        context = Context({
            'name': self.name,
            'link': link,
            'sender': self.sender.username,
            })
        message = template.render(context)
        send_mail(
                subject, message,
                settings.DEFAULT_FROM_EMAIL, [self.email]
                )

