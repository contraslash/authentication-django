from django.db import models
from django.contrib.auth.models import User

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
    role = models.ForeignKey(Role)

    def __unicode__(self):
        return unicode(self.user)


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

    def __unicode__(self):
        return self.name

