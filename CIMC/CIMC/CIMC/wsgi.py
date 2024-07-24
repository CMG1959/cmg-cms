"""
WSGI config for CIMC project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CIMC.settings")

application = get_wsgi_application()
#
# def application(environ, start_response):
#     if environ['mod_wsgi.process_group'] != '':
#         import signal
#         os.kill(os.getpid(), signal.SIGINT)
#     return ["killed"]