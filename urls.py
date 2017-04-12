# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # Log in
    url(
        r'log-in/$',
        auth_views.LoginView.as_view(
            template_name="authentication/log-in.html"
        ),
        name='log_in'
    ),

    url(
        r'log-out/$',
        auth_views.LogoutView.as_view(
            next_page="/"
        ),
        name='log_out'
    ),

    # Sign Up
    url(
        r'sign-up/$',
        views.SignUp.as_view(),
        name='sign_up'
    ),
    url(
        r'sign-up-confirm/(?P<token>\w+)/$',
        views.SignUpConfirm.as_view(),
        name='sign_up_confirm'
    ),

    # Change Password
    url(
        r'change-password/$',
        auth_views.PasswordChangeView.as_view(
            template_name="authentication/change-password.html"
        ),
        name='password_change'
    ),
    url(
        r'change-password-done/$',
        auth_views.PasswordChangeDoneView.as_view(
            template_name="authentication/change-password-success.html"
        ),
        name='password_change_done'
    ),

    # Password Recovery
    url(
        r'recover-password/$',
        auth_views.PasswordResetView.as_view(
            template_name="authentication/recover-password.html",
            html_email_template_name="authentication/email-restore-password.html",
        ),
        name='password_reset'
    ),
    url(
        r'recover-password-done/$',
        auth_views.PasswordResetDoneView.as_view(
            template_name="authentication/recover-password-success.html"
        ),
        name='password_reset_done'
    ),


    url(
        r'reset-password/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.PasswordResetConfirmView.as_view(template_name="authentication/reset-password.html"),
        name='password_reset_confirm'
    ),
    url(
        r'reset-password-done/$',
        auth_views.PasswordResetDoneView.as_view(template_name="authentication/change-password-success.html"),
        name='password_reset_complete'
    ),


]
