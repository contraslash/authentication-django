#! -*- encoding: UTF-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """
    Mixin genérico para obligar a un usuario a autenticarse antes de ver información del sistema
    """
    login_url = "log_in"
