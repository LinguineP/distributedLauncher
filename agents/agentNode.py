import agentModules.agentMessaging as msg
import agentModules.agentOps as ops
import time

masterIpStore={}
masterIpKey='masterIp'

def discovery():
    master_ip=ops.connect()
    masterIpStore[masterIpKey]=master_ip

def agentProcess():
    while True:
        #TODO: ping master address change
        if masterIpKey not in masterIpStore:
            discovery()
        print("hello i am ready for routine")
        time.sleep(10)



if __name__ == "__main__":
    
    agentProcess()