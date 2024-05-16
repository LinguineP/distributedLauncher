import utils
import agentMessaging as msg
from shellInteract import *





def launch_script(handler,cmd):
    handler.send_command(cmd) #runs the actual script
    handler.read_output()   #shows the script output
    handler.send_command('k') #handles the press any key to continue

def decent_start(script,numberOfNodes,currentNodeId,masterNodeIp):
    handler=ShellHandler()
    
    runDecentCmd = (f'{handler.pythonCmd}' f' ' 
                    f"{utils.find_script( utils.escape_chars(agentConfig.cfg['baseProjectPath']),script)}" f' '
                    f'{numberOfNodes}' f' '
                    f'{currentNodeId}' f' '
                    f'{masterNodeIp}' )
    
    launch_script(handler,runDecentCmd)


    

def cent_start(script,numberOfNodes,currentNodeId,masterNodeId,masterNodeIp):
    
    handler=ShellHandler()
    
    runDecentCmd = (f'{handler.pythonCmd}' f' ' 
                    f"{utils.find_script( utils.escape_chars(agentConfig.cfg['baseProjectPath']),script)}" f' '
                    f'{numberOfNodes}' f' '
                    f'{currentNodeId}' f' '
                    f'{masterNodeId}' f' '
                    f'{masterNodeIp}' )
    
    launch_script(handler,runDecentCmd)



def start_node(script,numberOfNodes,currentNodeId,masterNodeId,masterNodeIp,decent):
    print("node started")
    print(script,numberOfNodes,masterNodeId,currentNodeId,masterNodeIp,decent)
    

    
    if decent:
        decent_start(script,numberOfNodes,currentNodeId,masterNodeIp)
    else:
        cent_start(script,numberOfNodes,currentNodeId,masterNodeId,masterNodeIp)



def connect():
    masterIp=msg.receive_ip_from_multicast()    
    msg.send_hello()
    return masterIp

def wait_for_instructions():
    #TODO start command reaction

    received=msg.receive_command()
    if received['message']=="start_node":
        start_node(received['script'],
                   received['numberOfNodes'],
                   received['currentNodeId'],
                   received['masterNodeId'],
                   received['masterNodeIp'],
                   received['decent'])
    elif received['message']=="shutdown_agent":
        print("Shutting down the agent...")
        ShellHandler().close_shell()
        return False
    elif received['message']=="alive_ping":
        #TODO:check which nodes crashed
        pass
    else:
        print("Unknown command")
    
    return True


