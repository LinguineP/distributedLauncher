
import os
from config import *







def encription():
    pass

def decription():
    pass


def authentication_hello(rcv_message):
    if rcv_message['message']!=cfg['authentication']['stored_hello_message'] or rcv_message['pass']!=cfg['authentication']['stored_hello_pass']:
        print("Wrong credentials")
        return False
    return True


def get_files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)) and file.endswith('.py') and not file.startswith(('.', '_')):
            yield file

def getAvailableScripts():
    scripts=[] #it is assumed that the the script names are consistent across nodes, there are no duplicate scripts and proper paths  to scripts are given in cfg
    for path in cfg['scriptPaths']:
        scripts.extend(get_files(path))
    
    return scripts

def formStartMessage():
    pass


def hello_processing(hello_message):

    if not hello_message:
        return False,{}

    hello_keys=['hostname','ip','message','pass']
    
    if not all(key in hello_message for key in hello_keys):
        print("Incoming message format not Ok")
        return False,{}
    

    if not authentication_hello(hello_message):
        return False,{}
    
    all(map(hello_message.pop,['message','pass']))  

    return True,hello_message





