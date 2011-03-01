import os
import getpass

#from fabric.api import *
from fabric.api import env, sudo, require, local, cd, run, settings, prompt

from fabric.contrib import files
from fabric import utils

def _setup_path():
    # TODO: something like
    # if not defined env.project_subdir:
    #     env.project_subdir = env.project
    # env.project_root    = os.path.join(env.home, env.project_subdir)

    # allow for the fabfile having set up some of these differently
    if not env.has_key('project_root'):
        env.project_root    = os.path.join(env.home, env.project_dir)
    if not env.has_key('vcs_root'):
        env.vcs_root        = os.path.join(env.project_root, 'dev')
    if env.project_type == "django" and not env.has_key('django_root'):
        env.django_root     = os.path.join(env.vcs_root, env.django_dir)
    if env.use_virtualenv:
        if not env.has_key('virtualenv_root'):
            env.virtualenv_root = os.path.join(env.project_root, 'env')
        if not env.has_key('python_bin'):
            env.python_bin      = os.path.join(env.virtualenv_root, 'bin', 'python26')
    if not env.has_key('settings'):
        env.settings        = '%(project)s.settings' % env

def _get_svn_user_and_pass():
    if not env.has_key('svnuser') or len(env.svnuser) == 0:
        # prompt user for username
        prompt('Enter SVN username:', 'svnuser')
    if not env.has_key('svnpass') or len(env.svnpass) == 0:
        # prompt user for password
        env.svnpass = getpass.getpass('Enter SVN password:')



def deploy_clean(revision=None):
    """ delete the entire install and do a clean install """
    if env.environment == 'production':
        utils.abort('do not delete the production environment!!!')
    require('project_root', provided_by=env.valid_non_prod_envs)
    sudo('rm -rf %s' % env.project_root)
    deploy(revision)


def deploy(revision=None):
    """ update remote host environment (virtualenv, deploy, update) """
    require('project_root', provided_by=env.valid_envs)
    if not files.exists(env.project_root):
        sudo('mkdir -p %(project_root)s' % env)
    if env.use_virtualenv:
        create_virtualenv()
    checkout_or_update(revision)
    if env.use_virtualenv:
        update_requirements()
    if env.project_type == "django":
        link_local_settings()
        update_db()
    link_apache_conf()
    apache_restart()


def local_test():
    """ run the django tests on the local machine """
    require('project')
    with cd(os.path.join("..", env.project)):
        local("python " + env.test_cmd, capture=False)


def remote_test():
    """ run the django tests remotely - staging only """
    require('django_root', 'python_bin', 'test_cmd', provided_by=env.valid_non_prod_envs)
    with cd(env.django_root):
        sudo(env.python_bin + env.test_cmd)


def create_virtualenv():
    """ setup virtualenv on remote host """
    require('virtualenv_root', provided_by=env.valid_envs)
    if files.exists(os.path.join(env.virtualenv_root, 'bin')):
        # virtualenv already exists
        return
    # note these args are for centos 5 as set up by puppet
    args = '--clear --python /usr/bin/python26 --no-site-packages --distribute'
    sudo('virtualenv %s %s' % (args, env.virtualenv_root))


def checkout_or_update(revision=None):
    """ checkout the project from subversion """
    require('project_root', 'repo_type', 'vcs_root', 'repository',
        provided_by=env.valid_envs)
    if env.repo_type == "svn":
        # function to ask for svnuser and svnpass
        _get_svn_user_and_pass()
        # if the .svn directory exists, do an update, otherwise do
        # a checkout
        if files.exists(os.path.join(env.vcs_root, ".svn")):
            cmd = 'svn update --username %s --password %s' % (env.svnuser, env.svnpass)
            if revision:
                cmd += " --revision " + revision
            with cd(env.vcs_root):
                with hide('running'):
                    sudo(cmd)
        else:
            cmd = 'svn checkout --username %s --password %s %s' % (env.svnuser, env.svnpass, env.repository)
            if revision:
                cmd += "@" + revision
            with cd(env.project_root):
                with hide('running'):
                    sudo(cmd)
    elif env.repo_type == "git":
        # if the .git directory exists, do an update, otherwise do
        # a clone
        if files.exists(os.path.join(env.vcs_root, ".git")):
            with cd(env.vcs_root):
                sudo('git pull')
        else:
            with cd(env.project_root):
                sudo('git clone %s dev' % env.repository)
        if revision:
            with cd(env.project_root):
                sudo('git checkout %s' % revision)


def update_requirements():
    """ update external dependencies on remote host """
    require('vcs_root', 'virtualenv_root', provided_by=env.valid_envs)

    cmd_base = ['source %(virtualenv_root)s/bin/activate; ' % env]
    cmd_base += ['pip install']
    cmd_base += ['-E %(virtualenv_root)s' % env]

    cmd = cmd_base + ['--requirement %s' % os.path.join(env.vcs_root, 'deploy', 'pip_packages.txt')]
    sudo(' '.join(cmd))

    # mysql is not normally installed on development machines,
    # let's ensure it is installed
    # TODO: check if this is installed and only install if required
    cmd = cmd_base + ['MySQL-python']
    sudo(' '.join(cmd))


def _get_django_db_settings():
    with cd(os.path.join(env.vcs_root, 'deploy')):
        db_details = run(env.python_bin + ' ' + 'get_db_details.py')
    db_name, db_user, db_pw = db_details.split(' ')
    return (db_name, db_user, db_pw)

def _get_mysql_root_password():
    # first try to read the root password from a file
    # otherwise ask the user
    with settings(warn_only=True):
        file_exists = sudo('test -f /root/mysql_root_password')
    if file_exists.failed:
        return getpass.getpass('Enter MySQL root password:')
    else:
        return sudo ('cat /root/mysql_root_password')

def update_db():
    """ create and/or update the database, do migrations etc """
    require('django_root', 'python_bin', provided_by=env.valid_envs)
    # first work out the database username and password
    db_name, db_user, db_pw = _get_django_db_settings()
    # then see if the database exists
    with settings(warn_only=True):
        db_exist = run('mysql -u %s -p%s %s -e "quit"' % 
                       (db_user, db_pw, db_name))
    if db_exist.failed:
        # create the database and grant privileges
        root_pw = _get_mysql_root_password()
        sudo('mysql -u root -p%s -e "CREATE DATABASE %s CHARACTER SET utf8"' % (root_pw, db_name))
        sudo('mysql -u root -p%s -e "GRANT ALL PRIVILEGES ON %s.* TO \'%s\'@\'localhost\' IDENTIFIED BY \'%s\'"' % 
            (root_pw, db_name, db_user, db_pw))
    # if we are using South we need to do the migrations aswell
    use_migrations = False
    for app in env.django_apps:
        if files.exists(os.path.join(env.django_root, app, 'migrations')):
            use_migrations = True
    with cd(env.django_root):
        sudo(env.python_bin + ' manage.py syncdb --noinput')
        if use_migrations:
            sudo(env.python_bin + ' manage.py migrate --noinput')

def touch():
    """ touch wsgi file to trigger reload """
    require('vcs_root', provided_by=env.valid_envs)
    wsgi_dir = os.path.join(env.vcs_root, 'wsgi')
    sudo('touch ' + os.path.join(wsgi_dir, 'wsgi_handler.py'))


def link_local_settings():
    """link the apache.conf file"""
    require('django_root', provided_by=env.valid_envs)
    # ensure that we create a local_settings.py using a link
    # eg. 'ln -s local_settings.py.staging local_settings.py'
    local_settings_path = os.path.join(env.django_root, 'local_settings.py')
    local_settings_env_path = local_settings_path + '.' + env.environment
    if not files.exists(local_settings_env_path):
        utils.abort('%s does not exist - you need a local_settings file for this environment' % local_settings_env_path)
    if not files.exists(local_settings_path):
        with cd(env.django_root):
            sudo('ln -s local_settings.py.' + env.environment + ' local_settings.py')
    # touch the wsgi file to reload apache
    touch()


def link_apache_conf():
    """link the apache.conf file"""
    require('vcs_root', provided_by=env.valid_envs)
    conf_file = os.path.join(env.vcs_root, 'apache', env.environment+'.conf')
    apache_conf = os.path.join('/etc/httpd/conf.d', env.project+'_'+env.environment+'.conf')
    if not files.exists(conf_file):
        utils.abort('No apache conf file found - expected %s' % conf_file)
    if not files.exists(apache_conf):
        sudo('ln -s %s %s' % (conf_file, apache_conf))
    configtest()


def configtest():    
    """ test Apache configuration """
    sudo('/usr/sbin/httpd -S')


def apache_reload():    
    """ reload Apache on remote host """
    sudo('/etc/init.d/httpd reload')


def apache_restart():    
    """ restart Apache on remote host """
    sudo('/etc/init.d/httpd restart')



