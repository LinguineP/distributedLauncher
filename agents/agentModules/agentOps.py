import agentMessaging as msg


def start_node(script,numberOfNodes,masterNodeId,currentNodeId,masterNodeIp,decent):
    print("node started")
    print(script,numberOfNodes,masterNodeId,currentNodeId,masterNodeIp,decent)

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
                   received['masterNodeId'],
                   received['currentNodeId'],
                   received['masterNodeIp'],
                   received['decent'])
    elif received['message']=="shutdown_agent":
        print("Shutting down the agent...")
        return False
    elif received['message']=="alive_ping":
        #todo:check which nodes crashed
        pass
    else:
        print("Unknown command")
    
    return True
    