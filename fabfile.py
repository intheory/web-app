###################################
# Fab file to deploy these app    #
# to various servers.             #
# Author: Giorgos Eracleous       #
###################################

import os
from fabric.api import *
from fabric.colors import green

env.project = 'intheory'
env.user = 'george'
code_dir = '/www/virtualenv/intheory/src/'
env.hosts = ['intheory.co.uk:8080']

####################
# PROCESS COMMANDS #
####################

def start():
    '''
    Starts the server.
    '''
    local("python app.py")
    print(green("Server started!"))


def restart():
   sudo('supervisorctl restart tornadoes:')

def pull():
        with cd(code_dir):
                sudo("sudo git pull origin master")

def deploy():
        sudo('supervisorctl stop tornadoes:')
        pull()
        sudo('sudo pip install -r pip-reqs.txt')
        sudo('supervisorctl start tornadoes:')

def status():
        sudo('supervisorctl status')
