#! -*- encoding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db import IntegrityError

from base import utils

from . import conf as authentication_conf


class Role(models.Model):
    """
    Model for role system
    """

    # Name of the role
    name = models.CharField(max_length=100)
    # Short name, used for better results in queries
    short_name = models.CharField(max_length=100, blank=True, null=True)
    # Description of actions for this role
    description = models.TextField()

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):
    """
    Model for extended information of User at django.contrib.auth
    """

    # One to one references to User Model
    user = models.OneToOneField(User)
    # Activation toke for email verification
    activation_token = models.CharField(max_length=40, blank=True)
    # Expiration date for activation token
    expiration = models.DateTimeField(blank=True, null=True)
    # Role in system for this user
    role = models.ForeignKey(Role, blank=True, null=True)

    # Slug
    slug = models.SlugField(blank=True)
    # profile_image
    image = models.ImageField(blank=True, null=True, upload_to=authentication_conf.UPLOAD_PROFILE_IMAGES)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.slug:
            self.slug = slugify(self.user.username)
        successful_save = False
        saved_object = None
        while not successful_save:
            try:
                saved_object = super(UserProfile, self).save(force_insert, force_update, using, update_fields)
                successful_save = True
            except IntegrityError:
                self.slug = self.slug[:-4] + "-" + utils.generate_random_string(4)
        return saved_object

    def __str__(self):
        return str(self.user)


class Permission(models.Model):
    """
    Model for permission custom implementation
    """
    # Many to many relation to Rol
    role = models.ManyToManyField(Role)
    # Short name, used for better results in queries
    short_name = models.CharField(max_length=100)
    # Name of the permission
    name = models.CharField(max_length=100)
    # Description of permission
    description = models.TextField()
    # Reverse name of url
    reverse_lazy_url = models.CharField(max_length=150)

    def __str__(self):
        return self.name

