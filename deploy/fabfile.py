# this is our common file that can be copied across projects
# we deliberately import all of this to get all the commands it
# provides as fabric commands
import os
from fabric.api import env, sudo, require, cd, settings
from fabric.contrib import files
from fabric.context_managers import hide

from fablib import apache_cmd, apache_reload, apache_restart, \
             checkout_or_update, clean_db, configtest, deploy_clean, \
             link_apache_conf, link_local_settings, local_test, remote_test, \
             setup_db_dumps, touch, update_db, update_requirements
import fablib

env.home = '/var/django/'
env.project = 'sarpaminfohub'
# the top level directory on the server
env.project_dir = env.project

# repository type can be "svn" or "git"
env.repo_type = "git"
env.repository = 'git://github.com/aptivate/' + env.project + '.git'
env.fixtures_repo = "https://svn.aptivate.org/svn/reactionsarpam/data/fixtures/"
env.svnuser = ""
env.svnpass = ""

env.django_dir = "django/" + env.project
env.django_apps = ['infohub', 'contactlist']
env.test_cmd = ' manage.py test -v0 ' + ' '.join(env.django_apps)


# put "django" here if you want django specific stuff to run
# put "plain" here for a basic apache app
env.project_type = "django"

# does this virtualenv for python packages
env.use_virtualenv = True

env.use_apache = True

# valid environments - used for require statements in fablib
env.valid_non_prod_envs = ('dev_server', 'staging_test', 'staging')
env.valid_envs = ('dev_server', 'staging_test', 'staging', 'production')


# this function can just call the fablib _setup_path function
# or you can use it to override the defaults
def _local_setup():
    # put your own defaults here
    fablib._setup_path()
    # override settings here
    # if you have an ssh key and particular user you need to use
    # then uncomment the next 2 lines
    #env.user = "root" 
    #env.key_filename = ["/home/shared/keypair.rsa"]
    env.fixtures_dir = os.path.join(env.django_root, "fixtures")


#
# These commands set up the environment variables
# to be used by later commands
#

def dev_server():
    """ use dev environment on remote host to play with code in production-like env"""
    env.environment = 'dev_server'
    env.hosts = ['fen-vz-sarpaminfohub-dev']
    _local_setup()


def staging_test():
    """ use staging environment on remote host to run tests"""
    # this is on the same server as the customer facing stage site
    # so we need project_root to be different ...
    env.project_dir = env.project + '_test'
    env.environment = 'staging_test'
    env.hosts = ['fen-vz-sarpaminfohub']
    _local_setup()


def staging():
    """ use staging environment on remote host to demo to client"""
    env.environment = 'staging'
    env.hosts = ['fen-vz-sarpaminfohub']
    _local_setup()


def production():
    """ use production environment on remote host"""
    env.environment = 'production'
    env.hosts = ['lin-sarpam.aptivate.org:48001']
    _local_setup()


def deploy(revision=None):
    """ update remote host environment (virtualenv, deploy, update) """
    require('project_root', provided_by=env.valid_envs)
    with settings(warn_only=True):
        apache_cmd('stop')
    if not files.exists(env.project_root):
        sudo('mkdir -p %(project_root)s' % env)
        
    checkout_or_update(revision)
    fablib._get_svn_user_and_pass()
    
    with hide('running'):
        sudo(env.tasks_bin + ' checkout_or_update_fixtures:svnuser=' + 
             env.svnuser + ',svnpass=' + env.svnpass)
    update_requirements()
    link_local_settings()
    create_search_dir()
    update_db()
    create_cache_table()
    if env.environment == 'production':
        setup_db_dumps()
    sudo(env.tasks_bin + ' load_fixtures')
    link_apache_conf()
    apache_cmd('start')
        
def create_search_dir():
    """Allow Apache to write to files in the search index directory"""
    require('django_root', provided_by=env.valid_envs)
    search_dir = os.path.join(env.django_root, "search_index")
    sudo("mkdir -p %s" % search_dir)
    sudo("chown -R apache:apache %s" % search_dir)
    # sudo("chown apache:apache %s/*" % search_dir)

def create_cache_table():
    sudo(env.tasks_bin + ' create_cache_table')
