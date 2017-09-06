from . import conf


def authentication_urls(request):
    return {
        "log_in_url": conf.LOGIN_URL,
        "log_out_url": conf.LOGOUT_URL,
        "sign_up_url": conf.SIGNUP_URL,
        "password_reset_url": conf.RESET_PASSWORD_URL
    }