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
print(PROJECT_DIR)
ROOT_DIR = os.path.dirname(PROJECT_DIR)
print(ROOT_DIR)
APPS_DIR = os.path.join(ROOT_DIR, 'slack')
print(APPS_DIR)
LIB_DIR = os.path.join(ROOT_DIR, 'myvenv/lib/python3.4/site-packages')
print(LIB_DIR)

sys.path.insert(0, PROJECT_DIR)
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, APPS_DIR)
sys.path.insert(0, LIB_DIR)

# sys.path.append('/var/www/SlackMarket/myvenv/lib/python3.4/site-packages')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.prod")


from django.core.wsgi import get_wsgi_application
import time
import traceback
import signal

# application = get_wsgi_application()
try:
    application = get_wsgi_application()
    print('WSGI without exception')
except Exception:
    print('handling WSGI exception')
    # Error loading applications
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)

