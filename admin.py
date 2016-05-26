from django.contrib import admin
from django.contrib.auth.models import  Permission

from . import models as authentication_models
# Register your models here.
admin.site.register(authentication_models.UserProfile)
admin.site.register(authentication_models.Role)
admin.site.register(authentication_models.Permission)
admin.site.register(Permission)
