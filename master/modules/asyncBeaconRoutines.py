import asyncio
import time
import messagingHandler as msg
import dbAdapter
from config import cfg

db_adapter = dbAdapter.SQLiteDBAdapter()


def beacon_process(stop_event):
    asyncio.run(beacon(stop_event))


async def beacon(stop_event):
    while not stop_event.is_set():
        msg.send_ip_to_multicast()
        time.sleep(2)


def incomingListener_process(stop_event, pipe_end):

    asyncio.run(incomingListener(stop_event, pipe_end))


async def incomingListener(stop_event, pipe_end):
    inNodes = []
    while not stop_event.is_set():
        success, result = hello_processing(msg.receive_discovery())
        if success:
            inNodes.append(result)
            print("number of discovered nodes", len(inNodes))
            db_adapter.nodes.create_new_node(result["hostname"], result["ip"])

    pipe_end.send(inNodes)


def getAvailableScripts():
    return getAvailableScripts()


def stop_beacon(stop_event):
    print("Stopping worker...")
    stop_event.set()


def authentication_hello(rcv_message):
    if (
        rcv_message["message"] != cfg["authentication"]["stored_hello_message"]
        or rcv_message["pass"] != cfg["authentication"]["stored_hello_pass"]
    ):
        print("Wrong credentials")
        return False
    return True


def hello_processing(hello_message):

    if not hello_message:
        return False, {}

    hello_keys = ["hostname", "ip", "message", "pass"]

    if not all(key in hello_message for key in hello_keys):
        print("Incoming message format not Ok")
        return False, {}

    if not authentication_hello(hello_message):
        return False, {}

    # removes message and pass key value pairs from dict
    all(map(hello_message.pop, ["message", "pass"]))

    return True, hello_message
