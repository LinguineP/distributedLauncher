import agentModules.agentMessaging as msg
import agentModules.agentOps as ops
import time

masterIpStore={}
masterIpKey='masterIp'

def discovery():
    master_ip=ops.connect()
    masterIpStore[masterIpKey]=master_ip

def execution():
    return ops.wait_for_instructions()

def agentProcess():
    agent_active=True
    while agent_active:
        #TODO: ping master address change
        if masterIpKey not in masterIpStore:
            discovery()
        
        agent_active=execution() 

        

        



if __name__ == "__main__":
    
    agentProcess()