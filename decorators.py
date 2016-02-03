from django.http import  HttpResponseForbidden
from django.template.loader import get_template
from django.core.urlresolvers import reverse_lazy

from . import models as authentication_models
def check_permissions(function):
    def inner_check(*args, **kwargs):
        request = None
        if kwargs.get('request', False):
            request = kwargs['request']
        else:
            for arg in args:
                if 'request' in arg.__class__.__name__.lower():
                    request = arg
        if request is not None:
            profile = authentication_models.UserProfile.objects.get(user=request.user)
            role = profile.role
            request_name = request.resolver_match.url_name
            permissions = authentication_models.Permission.objects.filter(role=role, reverse_lazy_url=request_name)

            print profile
            print role
            print request_name
            print permissions
            if not permissions:
                return HttpResponseForbidden(get_template('403.html').render({}))

        return function(*args, **kwargs)
    return inner_check
