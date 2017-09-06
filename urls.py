# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy

from django.contrib.auth import views as auth_views

from . import (
    views,
    conf
)

urlpatterns = [
    # Log in
    url(
        r'log-in/$',
        auth_views.LoginView.as_view(
            template_name="authentication/log-in.html"
        ),
        name=conf.LOGIN_URL
    ),

    url(
        r'log-out/$',
        auth_views.LogoutView.as_view(
            next_page="/"
        ),
        name=conf.LOGOUT_URL
    ),

    # Sign Up
    url(
        r'sign-up/$',
        views.SignUp.as_view(),
        name=conf.SIGNUP_URL
    ),
    url(
        r'sign-up-confirm/(?P<token>\w+)/$',
        views.SignUpConfirm.as_view(),
        name=conf.SIGNUP_CONFIRM_URL
    ),

    # Change Password
    url(
        r'change-password/$',
        auth_views.PasswordChangeView.as_view(
            template_name="authentication/change-password.html"
        ),
        name=conf.CHANGE_PASSWORD_URL
    ),
    url(
        r'change-password-done/$',
        auth_views.PasswordChangeDoneView.as_view(
            template_name="authentication/change-password-success.html"
        ),
        name=conf.CHANGE_PASSWORD_DONE_URL
    ),

    # Password Recovery
    url(
        r'recover-password/$',
        auth_views.PasswordResetView.as_view(
            template_name="authentication/recover-password.html",
            html_email_template_name="authentication/email-restore-password.html",
        ),
        name=conf.RESET_PASSWORD_URL
    ),
    url(
        r'recover-password-done/$',
        auth_views.PasswordResetDoneView.as_view(
            template_name="authentication/recover-password-success.html"
        ),
        name=conf.RESET_PASSWORD_DONE_URL
    ),


    url(
        r'reset-password/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.PasswordResetConfirmView.as_view(template_name="authentication/reset-password.html"),
        name=conf.RESET_PASSWORD_CONFIRM_URL
    ),
    url(
        r'reset-password-done/$',
        auth_views.PasswordResetDoneView.as_view(template_name="authentication/change-password-success.html"),
        name=conf.RESET_PASSWORD_COMPLETE_URL
    ),


]
