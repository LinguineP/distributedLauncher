import json
import socket
import random
import sys
import time
from agentConfig import *
import socket
import multicastSetup

multicastGroup = "239.255.10.1"  # viewRFC2365
multicastPort = 55001  # not a known port number
commPort = 55002
resultsPort = 55003
masterIp = ""
agentIp = ""
agentHostName = ""


def generate_offset():
    return random.uniform(0, 2)


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(
            ("10.255.255.255", multicastPort)
        )  # the address 10.255.255.255 is from the Private IP Address Range
        local_ip = s.getsockname()[0]
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        return local_ip
    except Exception as e:
        print("Error:", e)
        return None


def receive_ip_from_multicast():
    global masterIp, agentIp, agentHostName, multicastGroup

    # store for agents ip
    agentIp = get_local_ip()
    agentHostName = socket.gethostname()

    multicast_recv_socket = multicastSetup.MulticastSocket(
        multicastGroup, multicastPort, 1
    )
    print("Waiting for master node ip...")
    while True:
        try:
            data, source_addr = multicast_recv_socket.recvfrom()
            if data:
                masterIp = data.decode("utf-8")
                print(f"Master node IP address: {masterIp}")
                return masterIp
        except KeyboardInterrupt:
            print("\nCtrl+C pressed. Exiting...")
            exit(1)


def send_json(dest_ip, dest_port, data_dict):
    """sends json that is formed from a passed dict to specified address via tcp"""

    # Convert the dictionary to JSON
    json_data = json.dumps(data_dict)

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    print("Destination adress", dest_ip, dest_port)
    time.sleep(generate_offset())

    client_socket.connect((dest_ip, dest_port))

    # Send the JSON data
    client_socket.sendall(json_data.encode("utf-8"))
    print("Message sent.")

    client_socket.close()


def receive_command():
    """receives a command in the form of json via tcp"""

    agent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print()
    print("\nListening for commands from master node", masterIp, commPort)
    agent_socket.bind((agentIp, commPort))
    agent_socket.listen(1)

    try:
        master_socket, master_address = agent_socket.accept()

        json_data = receive_json(master_socket)
        print("Received command", json_data["message"])

        return json_data
    except Exception as e:
        print("Error:", e)
    finally:
        agent_socket.close()


def receive_json(socket: socket.socket):
    """receives a json on a passed socket"""
    data = b""
    while True:
        chunk = socket.recv(1024)
        if not chunk:
            break
        data += chunk

    json_data = json.loads(data.decode("utf-8"))
    return json_data


def sendResults(runOutput, runTime):
    results_msg = {
        "runOutput": runOutput,
        "runTime": runTime,
        "ip": agentIp,
        "hostname": agentHostName,
    }
    send_json(masterIp, resultsPort, results_msg)


def send_hello():
    """builds a hello command for and sends it to the master node"""
    hello_msg = {
        "message": cfg["authentication"]["stored_hello_message"],
        "pass": cfg["authentication"]["stored_hello_pass"],
        "ip": agentIp,
        "hostname": agentHostName,
    }
    print("\nSending a hello to the master node")
    send_json(masterIp, multicastPort, hello_msg)
