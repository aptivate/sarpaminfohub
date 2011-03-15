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

import tasklib

# import per-project settings
import project_settings

# are there any local tasks for this project?
try:
    import localtasks
except ImportError:
    localtasks = None

def invalid_command(cmd):
    print "Tasks.py:"
    print
    print "%s is not a valid command" % cmd
    print
    print "For help use --help"
    sys.exit(2)


def tasklib_list():
    tasks = []
    for task in dir(tasklib):
        if callable(getattr(tasklib, task)):
            if not task.startswith('_'):
                tasks.append(task)
    return tasks


def localtasks_list():
    if localtasks == None:
        return []
    tasks = []
    for task in dir(localtasks):
        if callable(getattr(localtasks, task)):
            if not task.startswith('_'):
                tasks.append(task)
    return tasks


def tasks_available():
    tasks = list(set(tasklib_list()+localtasks_list()))
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
            tasks = tasks_available()
            for task in tasks:
                print task
            print
            print "You can pass arguments by separating with a ':' For example:"
            print "./tasks.py link_local_settings:staging"
            sys.exit(0)
    # process arguments - just call the function with that name
    tasklib._setup_paths()
    for arg in args:
        task_bits = arg.split(':', 1)
        fname = task_bits[0]
        #print "fname = '%s'" % fname
        try:
            # work out which function to call - localtasks have priority
            f = None
            if fname in localtasks_list():
                f = getattr(localtasks, fname)
            elif fname in tasklib_list():
                f = getattr(tasklib, fname)
            else:
                invalid_command(fname)

            # call the function
            if len(task_bits) == 1:
                f()
            else:
                f_args = task_bits[1].split(',')
                pos_args = [arg for arg in f_args if arg.find('=') == -1]
                kwargs = [arg for arg in f_args if arg.find('=') >= 0]
                kwargs_dict = {}
                for kwarg in kwargs:
                    kw, value = kwarg.split('=', 1)
                    kwargs_dict[kw] = value
                f(*pos_args, **kwargs_dict)


if __name__ == '__main__':
    main()
