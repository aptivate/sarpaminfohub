# functions just for this project
import os
import getpass
import subprocess

import tasklib

# this is the svn repository that holds private fixtures
fixtures_repo = "https://svn.aptivate.org/svn/reactionsarpam/data/fixtures/"

import project_settings

def deploy(environment=None, svnuser=None, svnpass=None):
    if environment == None:
        environment = tasklib._infer_environment()

    tasklib.create_ve()
    tasklib.link_local_settings(environment)
    tasklib.update_db()
    checkout_or_update_fixtures(svnuser, svnpass)
    load_fixtures()

def run_jenkins(svnuser, svnpass):
    """ make sure the local settings is correct and the database exists """
    tasklib.update_ve()
    tasklib._install_django_jenkins()
    tasklib.link_local_settings('jenkins')
    tasklib.clean_db()
    tasklib.update_db()
    checkout_or_update_fixtures(svnuser, svnpass)
    load_fixtures()
    # for jenkins, link to sarpaminfohub directory so that we can read the nice
    # reports
    if not os.path.exists(os.path.join(tasklib.env['project_dir'], 'infohub')):
        subprocess.call(['ln', '-s', 'django/sarpaminfohub/infohub'], cwd=tasklib.env['project_dir'])
    if not os.path.exists(os.path.join(tasklib.env['project_dir'], 'contactlist')):
        subprocess.call(['ln', '-s', 'django/sarpaminfohub/contactlist'], cwd=tasklib.env['project_dir'])
    tasklib._manage_py_jenkins()


def checkout_or_update_fixtures(svnuser=None, svnpass=None):
    """ checkout the fixtures from subversion """
    if svnuser == None:
        # ask the user for svn username and password
        svnuser = raw_input('Enter SVN username:')
    if svnpass == None:
        svnpass = getpass.getpass('Enter SVN password:')

    fixtures_dir = os.path.join(tasklib.env['django_dir'], "fixtures")

    # if the .svn directory exists, do an update, otherwise do
    # a checkout
    if os.path.exists(os.path.join(fixtures_dir, ".svn")):
        cmd = ['svn', 'update', '--username', svnuser, '--password', svnpass]
        if tasklib.env['verbose']:
            print "Executing command: %s" % ' '.join(cmd)
        subprocess.call(cmd, cwd=fixtures_dir)
    else:
        cmd = ['svn', 'checkout', '--username', svnuser, '--password', svnpass, fixtures_repo]
        if tasklib.env['verbose']:
            print "Executing command: %s" % ' '.join(cmd)
        subprocess.call(cmd, cwd=tasklib.env['django_dir'])

def load_fixtures():
    # can't pass *.json to subprocess, so these 3 lines do *.json
    fixture_list = filter(lambda fn: fn.endswith('.json'), 
        os.listdir(os.path.join(tasklib.env['django_dir'], 'fixtures', 'initial_data')))
    fixture_list = map(lambda fn: os.path.join('fixtures', 'initial_data', fn), 
                        fixture_list)
    fixture_list.sort()
    tasklib._manage_py(['loaddata'] + fixture_list)

def create_cache_table():
    (db_engine, db_name, db_user, db_pw, db_port) = tasklib._get_django_db_settings()
    cache_table_name = 'sarpam_cache_table'
    tasklib._mysql_exec('DROP TABLE IF EXISTS %s.%s' % (db_name, cache_table_name))
    tasklib._manage_py(['createcachetable', cache_table_name])

def setup_profile_updates():
    project_name = project_settings.django_dir.split('/')[-1]
    cron_file = os.path.join('/etc', 'cron.daily', 'update_profiles_'+project_name)

    if not os.path.exists(cron_file):
        write_profile_updates_to_cron_file(cron_file)
        
def write_profile_updates_to_cron_file(cron_file):
    with open(cron_file, 'w') as f:
        f.write("#!/bin/sh\n")
        f.write("LOG_DIR=/var/log/update_profiles\n")
        f.write("LOG_FILE=${LOG_DIR}/update_profiles-`date +%m-%d`.log\n")
        f.write("EMAIL_CARERS=0\n")
        f.write("/usr/bin/curl --data \"\" http://localhost/contacts/batch_update/ > ${LOG_FILE} 2>&1\n")
        f.write("if [[ $? -ne 0 ]]; then\n")
        f.write("    echo *** FAILED TO UPDATE PROFILES ***\n")
        f.write("    echo\n")
        f.write("    EMAIL_CARERS=1\n")
        f.write("fi\n")
        f.write("if [[ ${EMAIL_CARERS} -ne 0 ]]; then\n")
        f.write("    cat ${LOG_FILE}\n")
        f.write("fi\n")
        
    os.chmod(cron_file, 0755)
