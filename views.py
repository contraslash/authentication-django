# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import ugettext as _
from django.template.loader import get_template
from django.template.context import Context
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.utils import timezone



from .forms import UserForm, User
from .models import UserProfile
from . import conf

from hashlib import sha1
from random import random
from datetime import datetime, timedelta

class SignUp(TemplateView):
    """
    Custom Sign up view. Sends a mail for email verification
    """
    template_name = 'authentication/sign-up.html'
    userform = UserForm(prefix='user')
    userformerrors = None
    send_confirmation_mail = False

    def get_context_data(self, **kwargs):
        context = super(SignUp, self).get_context_data(**kwargs)
        print context
        if 'userform' not in context:
            context['userform'] = self.userform
        if 'userformerrors' not in context:
            context['userformerrors'] = self.userformerrors
        return context

    def save_user(self, userform):
        if userform.is_valid():
            user = userform.save(commit=False)
            user.set_password(userform.cleaned_data['password'])
            user.save()
            return user
        return None

    def create_profile(self, user, role=None):
        username = user.username
        email = user.email

        salt = sha1(str(random())).hexdigest()[:5]

        activation_key = sha1(salt+email).hexdigest()

        today = timezone.make_aware(datetime.today(), timezone.get_current_timezone())
        key_expires = today + timedelta(2)

        # Get user by username
        user = User.objects.get(username=username)

        # Create and save user profile
        user_profile = UserProfile(user=user, activation_token=activation_key, expiration=key_expires, role=role)

        user_profile.save()

        return user_profile

    def send_mail(self, user_profile):
        activation_key = user_profile.activation_token
        email = user_profile.user.email

        # Send email with activation key

        url = "%s%s" % (
            conf.DOMAIN,
            reverse('sign_up_confirm', kwargs={
                'token': activation_key
            })
        )

        context = {
            'url': url
        }

        email_subject = conf.EMAIL_SUBJECT
        email_body = conf.EMAIL_BODY + url
        template = get_template('authentication/email-signup-confirmation.html')

        send_mail(
            email_subject,
            email_body,
            conf.EMAIL_FROM,
            [email],
            fail_silently=False,
            html_message=template.render(context))

    def post(self, request, *args, **kwargs):
        userform = UserForm(request.POST, prefix='user')
        user = self.save_user(userform)
        if user:
            user_profile = self.create_profile(user)

            if self.send_confirmation_mail:
                self.send_mail(user_profile)
                messages.add_message(self.request, messages.INFO, message=conf.CONFIRM_ACCOUNT)
                return HttpResponseRedirect(reverse_lazy('index'))
            else:
                user = authenticate(
                    username=request.POST.get('user-username', ''),
                    password=request.POST.get('user-password', '')
                )
                user.is_active = True
                user.save()
                login(self.request, user)
                return HttpResponseRedirect(reverse_lazy('index'))

        self.userformerrors = userform.errors
        return render(request, self.template_name, self.get_context_data(**kwargs))

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('index'))
        else:
            return render(request, self.template_name, self.get_context_data(**kwargs))


class SignUpConfirm(TemplateView):
    """
    Account verification view. Validates the token and activates the user for the platform
    """
    template_name = 'authentication/sign-up-confirm.html'

    def get(self, request, *args, **kwargs):

        if self.request.user.is_authenticated():
            HttpResponseRedirect(reverse_lazy('index'))
        try:
            activation_token = UserProfile.objects.get(activation_token=self.kwargs['token'])
        except UserProfile.DoesNotExist:
            return render(
                request,
                self.template_name,
                {
                    'status': conf.INVALID_URL
                }
            )

        if activation_token.expiration < timezone.now():
            return render(
                request,
                self.template_name,
                {
                    'status': conf.EXPIRED_URL
                }
            )

        user = activation_token.user
        user.is_active = True
        user.save()
        return render(
            request,
            self.template_name,
            {
                'status': conf.ACCOUNT_CONFIRMATION_SUCCESSFUL
            }
        )

