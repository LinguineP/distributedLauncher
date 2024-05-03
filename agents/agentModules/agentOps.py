import agentMessaging as msg




def connect():
    masterIp=msg.receive_ip_from_multicast()    
    msg.send_hello()
    return masterIp

def wait_for_instructions():
    #TODO start command reaction
    received=msg.receive_json()