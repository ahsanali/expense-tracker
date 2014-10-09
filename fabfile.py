# -*- coding: utf-8 -*-

# http://docs.fabfile.org/en/1.5/tutorial.html

from fabric.api import *

project = "Expense Tracker"

# the user to use for the remote commands
env.user = ''
# the servers where the commands are executed
env.hosts = ['']


def reset():
    """
    Reset local debug env.
    """
    local("python manage.py initdb")

def apt_get(*packages):
    sudo('apt-get -y --no-upgrade install %s' % ' '.join(packages), shell=False)

def setup():
    """
    Setup virtual env.
    """

    apt_get("python-pip python-dev postgresql-9.3")
    local("apt-get -y build-dep python-psycopg2")
    local("virtualenv env")
    activate_this = "env/bin/activate_this.py"
    execfile(activate_this, dict(__file__=activate_this))
    local("python setup.py install")
    reset()

def create_database():
    """Creates role and database"""
    db_user = 'expensetracker' # define these
    db_pass = 'beta'
    db_table = 'expensetracker'

    local('psql -U postgres -c "DROP ROLE IF EXISTS %s"'%db_user)
    local('psql -U postgres -c "CREATE USER %s WITH NOCREATEDB NOCREATEUSER ENCRYPTED PASSWORD E\'%s\'"' % (db_user, db_pass))
    local('psql -U postgres -c "DROP DATABASE IF EXISTS %s"'%db_table)
    local('psql -U postgres -c "CREATE DATABASE %s WITH OWNER %s"' % (
        db_table, db_user))

def d():
    """
    Debug.
    """

    reset()
    local("python manage.py run")



