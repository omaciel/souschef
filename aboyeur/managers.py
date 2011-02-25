# vim: ts=4 sw=4 expandtab ai
# -*- encoding: utf-8 -*-

from django.db import models

class RecipesManager(models.Manager):
    """
    Custom manager for the Snippet model.

    Adds shortcuts for common filtering operations, and for retrieving
    popular related objects.

    """
    def get_by_author(self, username):
        """
        Returns a QuerySet of Snippets submitted by a particular User.

        """
        return self.filter(author__username__exact=username)

    def get_by_category(self, category_slug):
        """
        Returns a QuerySet of Snippets written in a particular
        Language.

        """
        return self.filter(category__slug__exact=category_slug)

    def get_by_tag(self, tag_slug):
        """
        Returns a QuerySet of Snippets which have a particular Tag.

        """
        return self.filter(tags__slug__exact=tag_slug)
