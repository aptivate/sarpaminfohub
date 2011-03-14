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


def _manage_py(args):
    # if ve is not yet created then python_bin won't exist
    # so check before using manage.py
    if os.path.exists(env['python_bin']):
        manage_cmd = [env['python_bin'], 'manage.py']
    else:
        manage_cmd = ['/usr/bin/python2.6', 'manage.py']
    if isinstance(args, str):
        manage_cmd.append(args)
    else:
        manage_cmd.extend(args)
    popen = subprocess.Popen(manage_cmd, cwd=env['django_dir'], stdout=subprocess.PIPE,
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
            test_db_name = 'test_' + db_name
            # create the database and grant privileges
            root_pw = _get_mysql_root_password()
            mysql_cmd = 'CREATE DATABASE %s CHARACTER SET utf8' % db_name
            subprocess.call(['mysql', '-u', 'root', '-p'+root_pw, '-e', mysql_cmd])
            mysql_cmd = 'CREATE DATABASE %s CHARACTER SET utf8' % test_db_name
            subprocess.call(['mysql', '-u', 'root', '-p'+root_pw, '-e', mysql_cmd])
            mysql_cmd = ('GRANT ALL PRIVILEGES ON %s.* TO \'%s\'@\'localhost\' IDENTIFIED BY \'%s\'' % 
                (db_name, db_user, db_pw))
            subprocess.call(['mysql', '-u', 'root', '-p'+root_pw, '-e', mysql_cmd])
            mysql_cmd = ('GRANT ALL PRIVILEGES ON %s.* TO \'%s\'@\'localhost\' IDENTIFIED BY \'%s\'' % 
                (test_db_name, db_user, db_pw))
            subprocess.call(['mysql', '-u', 'root', '-p'+root_pw, '-e', mysql_cmd])
    # if we are using South we need to do the migrations aswell
    use_migrations = False
    for app in project_settings.django_apps:
        if os.path.exists(os.path.join(env['django_dir'], app, 'migrations')):
            use_migrations = True
    _manage_py(['syncdb', '--noinput'])
    if use_migrations:
        _manage_py(['migrate', '--noinput'])


def run_tests():
    args = ['test', '-v0']
    args.extend(project_settings.django_apps)
    _manage_py(args)


def prepare_jenkins():
    update_ve()
    # first we need to ensure that pip has installed the django-jenkins thing
    pip_bin = os.path.join(env['ve_dir'], 'bin', 'pip')
    cmd = [pip_bin, 'install', '-E', env['ve_dir'], 'django-jenkins']
    subprocess.call(cmd)
    # make sure the local settings is correct and the database exists
    link_local_settings('jenkins')
    update_db()
    # and now run jenkins
#    args = ['jenkins', ]
#    args.extend(project_settings.django_apps)
#    _manage_py(args)


def deploy(environment):
    """Do all the required steps in order"""
    create_ve()
    link_local_settings(environment)
    update_db()

def _invalid_command(cmd):
    print "Tasks.py:"
    print
    print "%s is not a valid command" % cmd
    print
    print "For help use --help"
    sys.exit(2)


def _localtasks_list():
    if localtasks == None:
        return []
    tasks = []
    for task in dir(localtasks):
        if callable(getattr(localtasks, task)):
            if not task.startswith('_'):
                if not task in localtasks.tasks_to_ignore:
                    tasks.append(task)
    return tasks


def _tasks_available(include_hidden=False):
    tasks_to_ignore = ['main', '_tasks_available', '_localtasks_list']
    tasks = _localtasks_list()
    for task in globals():
        if callable(globals()[task]):
            if not task.startswith('_'):
                if not task in tasks_to_ignore:
                    tasks.append(task)
    tasks.sort()
    return tasks

def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            print "The functions you can call are:"
            print
            for task in _tasks_available():
                print task
            print
            print "You can pass arguments by separating with a ':' For example:"
            print "./tasks.py link_local_settings:staging"
            sys.exit(0)
    # process arguments - just call the function with that name
    _setup_paths()
    for arg in args:
        task_bits = arg.split(':', 1)
        fname = task_bits[0]
        #print "fname = '%s'" % fname
        try:
            # work out which function to call
            f = None
            if fname in _localtasks_list():
                f = getattr(localtasks, fname)
            elif fname == 'main' or not callable(globals()[fname]):
                _invalid_command(fname)
            else:
                f = globals()[fname]

            # call the function
            if len(task_bits) == 1:
                f()
            else:
                f_args = task_bits[1]
                f(f_args)
        except KeyError:
            _invalid_command(fname)


if __name__ == '__main__':
    main()
