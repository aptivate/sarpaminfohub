#!/usr/bin/python2.6
#
# This script is to set up various things for our projects. It can be used by:
#
# * developers - setting up their own environment
# * jenkins - setting up the environment and running tests
# * fabric - it will call a copy on the remote server when deploying
#
# The tasks it will do (eventually) include:
#
# * creating, updating and deleting the virtualenv
# * creating, updating and deleting the database (sqlite or mysql)
# * setting up the local_settings stuff
# * running tests
"""This script is to set up various things for our projects. It can be used by:

* developers - setting up their own environment
* jenkins - setting up the environment and running tests
* fabric - it will call a copy on the remote server when deploying

"""

import os, sys
import getopt
import getpass
import subprocess 

# import per-project settings
import project_settings

# are there any local tasks for this project?
try:
    import localtasks
except ImportError:
    localtasks = None

env = {}

def _setup_paths():
    """Set up the paths used by other tasks"""
    # what is the root of the project - one up from this directory
    env['project_dir'] = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    env['django_dir']  = os.path.join(env['project_dir'], project_settings.django_dir)
    env['ve_dir']      = os.path.join(env['django_dir'], '.ve')
    env['python_bin']  = os.path.join(env['ve_dir'], 'bin', 'python2.6')
    env['manage_py']   = os.path.join(env['django_dir'], 'manage.py')


def _manage_py(args, cwd=None):
    # if ve is not yet created then python_bin won't exist
    # so check before using manage.py
    if os.path.exists(env['python_bin']):
        manage_cmd = [env['python_bin'], env['manage_py']]
    else:
        manage_cmd = ['/usr/bin/python2.6', env['manage_py']]
    if isinstance(args, str):
        manage_cmd.append(args)
    else:
        manage_cmd.extend(args)

    if cwd == None:
        cwd = env['django_dir']

    popen = subprocess.Popen(manage_cmd, cwd=cwd, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
    for line in iter(popen.stdout.readline, ""):
        print line,
    returncode = popen.wait()
    if returncode != 0:
        sys.exit(popen.returncode)


def _get_django_db_settings():
    # import local_settings from the django dir. Here we are adding the django
    # project directory to the path. Note that env['django_dir'] may be more than
    # one directory (eg. 'django/project') which is why we use django_module
    sys.path.append(env['django_dir'])
    import local_settings

    db_user = 'nouser'
    db_pw   = 'nopass'
    # there are two ways of having the settings:
    # either as DATABASE_NAME = 'x', DATABASE_USER ...
    # or as DATABASES = { 'default': { 'NAME': 'xyz' ... } }
    try:
        db = local_settings.DATABASES['default']
        db_engine = db['ENGINE']
        db_name   = db['NAME']
        if db_engine == 'mysql':
            db_user   = db['USER']
            db_pw     = db['PASSWORD']
    except (AttributeError, KeyError):
        try:
            db_engine = local_settings.DATABASE_ENGINE
            db_name   = local_settings.DATABASE_NAME
            if db_engine == 'mysql':
                db_user   = local_settings.DATABASE_USER
                db_pw     = local_settings.DATABASE_PASSWORD
        except AttributeError:
            # we've failed to find the details we need - give up
            print("Failed to find database settings")
            sys.exit(1)
    return (db_engine, db_name, db_user, db_pw)

def _get_mysql_root_password():
    # first try to read the root password from a file
    # otherwise ask the user
    file_exists = subprocess.call(['sudo', 'test', '-f', '/root/mysql_root_password'])
    if file_exists == 0:
        # note this requires sudoers to work with this - jenkins particularly ...
        root_pw = subprocess.Popen(["sudo", "cat", "/root/mysql_root_password"], 
                stdout=subprocess.PIPE).communicate()[0]
        return root_pw.rstrip()
    else:
        return getpass.getpass('Enter MySQL root password:')


def clean_ve():
    """Delete the virtualenv so we can start again"""
    subprocess.call(['rm', '-rf', env['ve_dir']])
    
    
def clean_db():
    """Delete the database for a clean start"""
    # first work out the database username and password
    db_engine, db_name, db_user, db_pw = _get_django_db_settings()
    # then see if the database exists
    if db_engine == 'sqlite':
        # delete sqlite file
        if os.path.isabs(db_name):
            db_path = db_name
        else:
            db_path = os.path.abspath(os.path.join(env['django_dir'], db_name))
        os.remove(db_path)
    elif db_engine == 'mysql':
        # DROP DATABASE
        root_pw = _get_mysql_root_password()
        mysql_cmd = 'DROP DATABASE IF EXISTS %s' % db_name
        subprocess.call(['mysql', '-u', 'root', '-p'+root_pw, '-e', mysql_cmd])
        test_db_name = 'test_' + db_name
        mysql_cmd = 'DROP DATABASE IF EXISTS %s' % test_db_name
        subprocess.call(['mysql', '-u', 'root', '-p'+root_pw, '-e', mysql_cmd])


def create_ve():
    """Create the virtualenv"""
    _manage_py("update_ve")
    
    
def update_ve():
    create_ve()


def link_local_settings(environment):
    # die if the correct local settings does not exist
    local_settings_env_path = os.path.join(env['django_dir'], 
                                    'local_settings.py.'+environment)
    if not os.path.exists(local_settings_env_path):
        print "Could not find file to link to: %s" % local_settings_env_path
        sys.exit(1)
    subprocess.call(['rm', 'local_settings.py'], cwd=env['django_dir'])
    subprocess.call(['ln', '-s', 'local_settings.py.'+environment, 'local_settings.py'], 
            cwd=env['django_dir'])


def update_db():
    # first work out the database username and password
    db_engine, db_name, db_user, db_pw = _get_django_db_settings()
    # then see if the database exists
    if db_engine == 'mysql':
        db_exist = subprocess.call(
                    ['mysql', '-u', db_user, '-p'+db_pw, db_name, '-e', 'quit'])
        if db_exist != 0:
            # create the database and grant privileges
            root_pw = _get_mysql_root_password()
            mysql_cmd = 'CREATE DATABASE %s CHARACTER SET utf8' % db_name
            subprocess.call(['mysql', '-u', 'root', '-p'+root_pw, '-e', mysql_cmd])
            mysql_cmd = ('GRANT ALL PRIVILEGES ON %s.* TO \'%s\'@\'localhost\' IDENTIFIED BY \'%s\'' % 
                (db_name, db_user, db_pw))
            subprocess.call(['mysql', '-u', 'root', '-p'+root_pw, '-e', mysql_cmd])

            # create the test database, grant privileges and drop it again
            test_db_name = 'test_' + db_name
            mysql_cmd = 'CREATE DATABASE %s CHARACTER SET utf8' % test_db_name
            subprocess.call(['mysql', '-u', 'root', '-p'+root_pw, '-e', mysql_cmd])
            mysql_cmd = ('GRANT ALL PRIVILEGES ON %s.* TO \'%s\'@\'localhost\' IDENTIFIED BY \'%s\'' % 
                (test_db_name, db_user, db_pw))
            subprocess.call(['mysql', '-u', 'root', '-p'+root_pw, '-e', mysql_cmd])
            mysql_cmd = ('DROP DATABASE %s' % test_db_name)
            subprocess.call(['mysql', '-u', 'root', '-p'+root_pw, '-e', mysql_cmd])
    # if we are using South we need to do the migrations aswell
    use_migrations = False
    for app in project_settings.django_apps:
        if os.path.exists(os.path.join(env['django_dir'], app, 'migrations')):
            use_migrations = True
    _manage_py(['syncdb', '--noinput'])
    if use_migrations:
        _manage_py(['migrate', '--noinput'])

def setup_db_dumps(dump_dir):
    """ set up mysql database dumps in root crontab """
    if not os.path.isabs(dump_dir):
        print 'dump_dir must be an absolute path, you gave %s' % dump_dir
        sys.exit(1)
    project_name = project_settings.django_dir.split('/')[-1]
    cron_file = os.path.join('/etc', 'cron.daily', 'dump_'+project_name)

    db_engine, db_name, db_user, db_pw = _get_django_db_settings()
    if db_engine == 'mysql':
        if not os.path.exists(dump_dir):
            subprocess.call(['mkdir', '-p', dump_dir])
        dump_file_stub = os.path.join(dump_dir, 'daily-dump-')

        # has it been set up already
        cron_grep = subprocess.call('sudo crontab -l | grep mysqldump', shell=True)
        if cron_grep == 0:
            return
        if os.path.exists(cron_file):
            return

        # write something like:
        # 30 1 * * * mysqldump --user=osiaccounting --password=aptivate --host=127.0.0.1 osiaccounting >  /var/osiaccounting/dumps/daily-dump-`/bin/date +\%d`.sql
        with open(cron_file, 'w') as f:
            f.write('#!/bin/sh\n')
            f.write('/usr/bin/mysqldump --user=%s --password=%s --host=127.0.0.1 %s > %s' %
                    (db_user, db_pw, db_name, dump_file_stub))
            f.write(r'`/bin/date +\%d`.sql')
            f.write('\n')
        os.chmod(cron_file, 0755)


def run_tests():
    args = ['test', '-v0']
    args.extend(project_settings.django_apps)
    _manage_py(args)


def _install_django_jenkins():
    """ ensure that pip has installed the django-jenkins thing """
    pip_bin = os.path.join(env['ve_dir'], 'bin', 'pip')
    cmd = [pip_bin, 'install', '-E', env['ve_dir'], 'django-jenkins']
    subprocess.call(cmd)

def _manage_py_jenkins():
    """ run the jenkins command """
    args = ['jenkins', ]
    args += ['--pylint-rcfile', os.path.join(env['project_dir'], 'jenkins', 'pylint.rc')]
    args += project_settings.django_apps
    _manage_py(args, cwd=env['project_dir'])

def run_jenkins():
    """ make sure the local settings is correct and the database exists """
    update_ve()
    _install_django_jenkins()
    link_local_settings('jenkins')
    clean_db()
    update_db()
    _manage_py_jenkins()


def _infer_environment():
    local_settings = os.path.join(env['django_dir'], 'local_settings.py')
    if os.path.exists(local_settings):
        return os.readlink(local_settings).split('.')[-1]
    else:
        print 'no environment set, or pre-existing'
        sys.exit(2)


def deploy(environment=None):
    """Do all the required steps in order"""
    if environment == None:
        environment = _infer_environment()

    create_ve()
    link_local_settings(environment)
    update_db()

