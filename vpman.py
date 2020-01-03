#!/usr/bin/env python3
''' DESCRIPTION
This is a simple script designed to make VPN management easier.
'''
from subprocess import run
from getpass import getpass
from os import geteuid
from tempfile import NamedTemporaryFile as ntf
from vpman_common import fatal as fatal
from vpman_config import main as vpconf
from vpman_select import main as vppick

def ovpn(conf, auth):
    '''Takes the location of a config file and a password 
    and runs openvpn. Automatically reconnects if the connection
    is dropped.'''
    while True:
        run(["ovpn", "--config", conf, "--auth-user-pass", auth])

def ask_echo():
    '''Ask if the user wants their password echoed or not.'''
    while True:
        x = input("Echo Password? [y/n]: ")
        if x in ("y","Y"):
            return True
        if x in ("N","n"):
            return False

def get_input(echo=True, msg=""):
    '''Get user input.'''
    print(msg)
    if echo == True:
        return input()
    if echo == False:
        return getpass(prompt="")

def check_root():
    if geteuid() != "0":
        fatal("This application needs to be run as root.")

def get_auth():
    '''Return a temporary file containing the user's
    name and password.'''
    user = get_input(msg="VPN username?")
    echo = ask_echo()
    pwrd = get_input(echo=echo, msg="VPN password?")
    temp = ntf(mode="w")
    temp.writelines([user,"\n",pwrd,"\n"])
    temp.flush()
    return temp

''' # Uncomment when finished.
auth = get_auth() # Make a temp file with username and password
ovpn(conf=conf, auth=auth.name) # Run openvpn
# '''

data = vpconf()
vppick(data)