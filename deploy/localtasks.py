# functions just for this project
import os
import getpass
import subprocess

tasks_to_ignore = []

def deploy(environment):
    import tasks
    tasks.create_ve()
    tasks.link_local_settings(environment)
    tasks.update_db()
    checkout_or_update_fixtures()
    load_fixtures()

def checkout_or_update_fixtures(svnuser=None, svnpass=None):
    """ checkout the fixtures from subversion """
    if svnauth == None:
        # ask the user for svn username and password
        svnuser = raw_input('Enter SVN username:')
    if svnpass == None:
        svnpass = getpass.getpass('Enter SVN password:')

    from tasks import env
    fixtures_dir = os.path.join(env['django_dir'], "fixtures")

    # if the .svn directory exists, do an update, otherwise do
    # a checkout
    if os.path.exists(os.path.join(fixtures_dir, ".svn")):
        cmd = ['svn', 'update', '--username', svnuser, '--password', svnpass]
        subprocess.call(cmd, cwd=fixtures_dir)
    else:
        cmd = ['svn', 'checkout', '--username', svnuser, '--password', svnpass, fixtures_repo]
        subprocess.call(cmd, cwd=env['django_root'])


def load_fixtures():
    import tasks
    tasks._manage_py(['loaddata', 'fixtures/initial_data/*.json'])
