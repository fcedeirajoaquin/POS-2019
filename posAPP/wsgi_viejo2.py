"""
WSGI config for posAPP project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""
import django
import os
import sys

path='/srv/http/pos'

if path not in sys.path:
  sys.path.append(path)
 
os.environ['DJANGO_SETTINGS_MODULE'] = 'posAPP.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
