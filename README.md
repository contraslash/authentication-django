# Authentication

Authentication is a simple django module that provides a simple wrapper for django.contrib.auth.views, 
adding a custom look and feel and a modified sign up method with email confirmation

To get this work, make sure you got the email configuration in you settings.py

An example for use Gmail SMTPs server:
```
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'myname@gmail.com'
EMAIL_HOST_PASSWORD = 'mypassword'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'nmyname@gmail.com'
```  

Also please edit the conf.py file, to customize your domain and other options

If you change the Strings Settings, remember to recompile the locales

```
./manage.py compilemessages
```

And edit the locale folder, for more information visit [our blog](http://blog.contraslash.com/creando-locales-con-django/).

Enjoy and feel free to put a ticket or write me to ma0@contraslash.com
