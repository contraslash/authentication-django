from django import template

from .. import models as authentication_models

register = template.Library()

@register.filter(name='check_perms')
def check_perms(user, reverse_url):
    role = authentication_models.UserProfile.objects.get(user=user).role
    return authentication_models.Permission.objects.filter(role=role, reverse_lazy_url=reverse_url)

@register.filter(name='get_role')
def get_role(user):
    return authentication_models.UserProfile.objects.get(user=user).role.short_name