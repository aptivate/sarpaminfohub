import os,sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", 'django')))

from sarpaminfohub import local_settings

# there are two ways of having the settings:
# either as DATABASE_NAME = 'x', DATABASE_USER ...
# or as DATABASES = { 'default': { 'NAME': 'xyz' ... } }

db_name = local_settings.DATABASE_NAME
db_user = local_settings.DATABASE_USER
db_pw   = local_settings.DATABASE_PASSWORD

print("%s %s %s" % (db_name, db_user, db_pw))
