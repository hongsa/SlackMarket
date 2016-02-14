# -*- coding: utf-8 -*-
"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(PROJECT_DIR)
APPS_DIR = os.path.join(ROOT_DIR, 'slack')


sys.path.insert(0, PROJECT_DIR)
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, APPS_DIR)
sys.path.append('/var/www/SlackMarket/myvenv/lib/python3.4/site-packages')

# sys.path.append('/var/www/SlackMarket/mysite')
# sys.path.append('/var/www/SlackMarket/slack')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.prod")


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


