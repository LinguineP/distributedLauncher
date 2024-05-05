import sys
import os
from shellInteract import *

def escape_chars(s):
    escape_dict = {'\\': '\\\\',
                   '\'': '\\\'',
                   '\"': '\\\"',
                   '\a': '\\a',
                   '\b': '\\b',
                   '\f': '\\f',
                   '\n': '\\n',
                   '\r': '\\r',
                   '\t': '\\t',
                   '\v': '\\v'}
    return "".join([escape_dict.get(char, char) for char in s])


def find_script(root_directory, target_file):
    for root, dirs, files in os.walk(root_directory):
        if target_file in files:
            return os.path.join(root, target_file)
        


def executeSetupCmds():

    handler=ShellHandler()
    if handler.shell_setup:
        return 
    
    print(f"ENV is setup: {handler.shell_setup} \n starting script .....")

    if  sys.platform != 'win32' and sys.platform != 'linux':
        print('Error:', sys.platform, 'is not supported!')
        exit(0)
    
    setupCmds=[]

    if sys.platform == 'win32':
        setupCmds.append(['venv_ptbfla/Scripts/activate'])   
        handler.pythonCmd="python"
    if sys.platform == 'linux':
        setupCmds.append(['source venv_ptbfla/bin/activate'])   
        handler.pythonCmd=f"python{sys.version_info.major}.{sys.version_info.minor}"


    for command in setupCmds:
        handler.send_command(command)
        handler.read_output()
    return True
            
