# this is our common file that can be copied across projects
# we deliberately import all of this to get all the commands it
# provides as fabric commands
from fabric.api import env
from fablib import apache_reload, apache_restart, checkout_or_update, \
             configtest, create_virtualenv, deploy_clean, \
             link_apache_conf, link_local_settings, local_test, remote_test, \
             touch, update_db, update_requirements
import fablib


env.home = '/var/django/'
env.project = 'sarpaminfohub'
# the top level directory on the server
env.project_dir = env.project

# repository type can be "svn" or "git"
env.repo_type = "git"
env.repository = 'git://github.com/aptivate/' + env.project + '.git'
env.fixtures_repo = "https://svn.aptivate.org/svn/reactionsarpam/data/fixtures/"

env.django_dir = "django/" + env.project
env.django_apps = ['infohub', ]
env.test_cmd = ' manage.py test -v0 ' + ' '.join(env.django_apps)


# put "django" here if you want django specific stuff to run
# put "plain" here for a basic apache app
env.project_type = "django"

# does this virtualenv for python packages
env.use_virtualenv = True

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
    utils.abort('remove this line when dev server setup')
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
    env.hosts = ['lin-sarpaminfohub.aptivate.org:48001']
    _local_setup()


def deploy(revision=None):
    """ update remote host environment (virtualenv, deploy, update) """
    require('project_root', provided_by=env.valid_envs)
    if not files.exists(env.project_root):
        sudo('mkdir -p %(project_root)s' % env)
    create_virtualenv()
    checkout_or_update(revision)
    checkout_or_update_fixtures()
    update_requirements()
    link_local_settings()
    update_db()
    link_apache_conf()
    apache_restart()

def checkout_or_update_fixtures():
    """ checkout the project from subversion """
    require('project_root', 'repo_type', 'vcs_root', 'repository',
        provided_by=env.valid_envs)
    # function to ask for svnuser and svnpass
    fablib._get_svn_user_and_pass()
    # if the .svn directory exists, do an update, otherwise do
    # a checkout
    if files.exists(os.path.join(env.fixtures_dir, ".svn")):
        cmd = 'svn update --username %s --password %s' % (env.svnuser, env.svnpass)
        with cd(env.fixtures_dir):
            sudo(cmd)
    else:
        cmd = 'svn checkout --username %s --password %s %s' % \
                        (env.svnuser, env.svnpass, env.fixtures_repo)
        with cd(env.django_root):
            sudo(cmd)

