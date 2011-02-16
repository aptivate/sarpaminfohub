import os, sys

project_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.abspath(os.path.join(project_dir, '../django')))
sys.path.append(os.path.abspath(os.path.join(project_dir, '../django/sarpaminfohub/')))

#print >> sys.stderr, sys.path

#sys.path.append('/var/sarpaminfohub-stage')

os.environ['DJANGO_SETTINGS_MODULE'] = 'sarpaminfohub.settings'
os.environ['PROJECT_NAME_HOME'] = '/var/django/sarpaminfohub/dev/django'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

