# -*- coding: utf-8 -*-

from hashlib import sha1
from random import random
from datetime import datetime, timedelta

from django.views import generic
from django.shortcuts import HttpResponseRedirect
from django.core.mail import send_mail
from django.template.loader import get_template
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.contrib.auth import (
    models as auth_models,
    views as auth_views
)
try:
    from django.core.urlresolvers import reverse_lazy, reverse
except ImportError:
    from django.urls import reverse_lazy, reverse


from . import (
    models,
    conf,
    mixins,
)


class Login(auth_views.LoginView):
    template_name = "{}/log-in.html".format(conf.AUTH_TEMPLATE_FOLDER)

    def get_context_data(self, **kwargs):
        context = super(Login, self).get_context_data(**kwargs)
        context['password_reset_allowed'] = conf.AUTH_ALLOW_PASSWORD_RECOVERY
        context['registration_allowed'] = conf.AUTH_ALLOW_SIGNUP
        return context


class SignUp(
    mixins.AlreadyAuthenticatedMixin,
    generic.CreateView
):
    """
    Custom Sign up view. Sends a mail for email verification
    """
    template_name = '{}/sign-up.html'.format(conf.AUTH_TEMPLATE_FOLDER)
    form_class = conf.AUTH_USER_SIGNUP_FORM

    send_confirmation_mail = conf.AUTH_VERIFY_EMAIL

    def get_context_data(self, **kwargs):
        context = super(SignUp, self).get_context_data(**kwargs)

        return context

    @staticmethod
    def save_user(userform):
        if userform.is_valid():
            user = userform.save(commit=False)
            user.set_password(userform.cleaned_data['password'])
            user.save()
            return user
        return None

    @staticmethod
    def create_profile(user):
        username = user.username
        email = user.email

        salt = sha1(str(random())).hexdigest()[:5]

        activation_key = sha1(salt+email).hexdigest()

        today = timezone.make_aware(datetime.today(), timezone.get_current_timezone())
        key_expires = today + timedelta(2)

        # Get user by username
        user = auth_models.User.objects.get(username=username)

        # Create and save user profile
        user_profile = models.UserProfile(
            user=user,
            activation_token=activation_key,
            expiration=key_expires
        )

        user_profile.save()

        return user_profile

    @staticmethod
    def send_mail(user_profile):
        activation_key = user_profile.activation_token
        email = user_profile.user.email

        # Send email with activation key

        url = "%s%s" % (
            conf.AUTH_DOMAIN,
            reverse(
                'sign_up_confirm',
                kwargs={
                    'token': activation_key
                })
        )

        context = {
            'url': url
        }

        email_subject = conf.AUTH_EMAIL_SUBJECT
        email_body = conf.AUTH_EMAIL_BODY + url
        template = get_template('{}/email-signup-confirmation.html'.format(conf.AUTH_TEMPLATE_FOLDER))

        send_mail(
            email_subject,
            email_body,
            conf.AUTH_EMAIL_FROM,
            [email],
            fail_silently=False,
            html_message=template.render(context))

    def form_valid(self, form):
        userform = form.save(commit=False)
        user = self.save_user(userform)
        user_profile = self.create_profile(user)

        if self.send_confirmation_mail:
            self.send_mail(user_profile)
            messages.add_message(self.request, messages.INFO, message=conf.AUTH_CONFIRM_ACCOUNT)
            return HttpResponseRedirect(reverse_lazy(conf.AUTH_INDEX_URL_NAME))
        else:
            print(user.username)
            print(user.password)
            user = authenticate(
                username=user.username,
                password=user.password
            )
            user.is_active = True
            user.save()
            login(self.request, user)
            return HttpResponseRedirect(reverse_lazy(conf.AUTH_INDEX_URL_NAME))


class SignUpConfirm(
    mixins.AlreadyAuthenticatedMixin,
    generic.TemplateView
):
    """
    Account verification view. Validates the token and activates the user for the platform
    """
    template_name = '{}/sign-up-confirm.html'.format(conf.AUTH_TEMPLATE_FOLDER)

    def get_context_data(self, **kwargs):
        context = super(SignUpConfirm, self).get_context_data(**kwargs)

        try:
            activation_token = models.UserProfile.objects.get(activation_token=self.kwargs['token'])
            if activation_token.expiration < timezone.now():
                context['status'] = conf.EXPIRED_URL
            else:
                user = activation_token.user
                user.is_active = True
                user.save()
                context['status'] = conf.AUTH_ACCOUNT_CONFIRMATION_SUCCESSFUL
        except models.UserProfile.DoesNotExist:
            context['status'] = conf.INVALID_URL

        return context
