#! /usr/bin/python
#! -*- coding: UTF-8 -*-
from django.utils.translation import ugettext_lazy as _

"""
URL NAMES and other important module global variables
"""
LOGIN_URL = "log_in"
LOGOUT_URL = "log_out"
SIGNUP_URL = "sign_up"
SIGNUP_CONFIRM_URL = "sign_up_confirm"
CHANGE_PASSWORD_URL = "change_password"
CHANGE_PASSWORD_DONE_URL = "password_change_done"
RESET_PASSWORD_URL = "password_reset"
RESET_PASSWORD_DONE_URL = "password_reset_done"
RESET_PASSWORD_CONFIRM_URL = "password_reset_confirm"
RESET_PASSWORD_COMPLETEURL = "password_reset_complete"

# Email Settings
EMAIL_FROM = "info@contraslash.com"
EMAIL_SUBJECT = _("Confirmation email")
EMAIL_BODY = _("Thanks for register, please, visit the next link to activate your account: ")

# Domain Settings
DOMAIN = "http://c4tk.contraslash.com"

# Messages Settings
CONFIRM_ACCOUNT = _("Please confirm your account")
ACCOUNT_CONFIRMATION_SUCCESSFUL = _('Your account has been activated')

INVALID_URL = _('Invalid URL')
EXPIRED_URL = _('Expired URL')