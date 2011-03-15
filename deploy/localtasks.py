# functions just for this project
import os
import getpass
import subprocess

import tasklib

# this is the svn repository that holds private fixtures
fixtures_repo = "https://svn.aptivate.org/svn/reactionsarpam/data/fixtures/"

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
    tasklib.update_db()
    checkout_or_update_fixtures(svnuser, svnpass)
    load_fixtures()
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
        subprocess.call(cmd, cwd=fixtures_dir)
    else:
        cmd = ['svn', 'checkout', '--username', svnuser, '--password', svnpass, fixtures_repo]
        subprocess.call(cmd, cwd=tasklib.env['django_dir'])


def load_fixtures():
    # can't pass *.json to subprocess, so these 3 lines do *.json
    fixture_list = filter(lambda fn: fn.endswith('.json'), 
        os.listdir(os.path.join(tasklib.env['django_dir'], 'fixtures', 'initial_data')))
    fixture_list = map(lambda fn: os.path.join('fixtures', 'initial_data', fn), 
                        fixture_list)
    fixture_list.sort()
    tasklib._manage_py(['loaddata'] + fixture_list)
