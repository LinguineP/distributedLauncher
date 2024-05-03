import asyncio
import time
import messagingHandler as msg 
from dataProcessing import * 


def beacon_process(stop_event):
    asyncio.run(beacon(stop_event))



async def beacon(stop_event):
    while not stop_event.is_set():
        msg.send_ip_to_multicast()
        time.sleep(2)

        
def incomingListener_process(stop_event,pipe_end):
    
    asyncio.run(incomingListener(stop_event,pipe_end))     

async def incomingListener(stop_event,pipe_end):
    inNodes=[]
    while not stop_event.is_set():
        success,result=hello_processing(msg.receive_discovery())
        #TODO filter by message and pass
        if success:
            inNodes.append(result)    
    pipe_end.send(inNodes)
    

def stop_beacon(stop_event):
    print("Stopping worker...")
    stop_event.set()




