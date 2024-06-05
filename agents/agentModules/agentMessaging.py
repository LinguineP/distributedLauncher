import json
import socket
from agentConfig import *
import socket
import multicastSetup

multicastGroup = "239.255.0.0"
portMulticast = 55001  # not a known port number
portComm = 55002
masterIp = ""


multicastGroup = "239.255.10.1"  # viewRFC2365
multicastPort = 55001  # not a known port number
commPort = 55002
masterIp = ""
agentIp = ""


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
    global masterIp, agentIp, multicastGroup

    # store for agents ip
    agentIp = get_local_ip()

    multicast_recv_socket = multicastSetup.MulticastSocket(
        multicastGroup, multicastPort
    )

    while True:
        data, source_addr = multicast_recv_socket.recvfrom()
        if data:
            masterIp = data.decode("utf-8")
            print(f"Received IP address: {masterIp}, {source_addr}")
            return masterIp


def master_ping():
    pass


def send_json(dest_ip, dest_port, data_dict):
    """sends json that is formed from a passed dict to specified address via tcp"""

    # Convert the dictionary to JSON
    json_data = json.dumps(data_dict)

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    print(dest_ip, dest_port)
    client_socket.connect((dest_ip, dest_port))
    print("Connected to server.")

    # Send the JSON data
    client_socket.sendall(json_data.encode("utf-8"))
    print("JSON data sent successfully.")

    client_socket.close()


def receive_command():
    """receives a command in the form of json via tcp"""

    agent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(masterIp, commPort)
    agent_socket.bind((agentIp, commPort))
    agent_socket.listen(1)

    try:
        master_socket, master_address = agent_socket.accept()

        json_data = receive_json(master_socket)

        return json_data
    except Exception as e:
        # print("Error:", e)
        pass
    finally:
        agent_socket.close()


def receive_json(socket):
    """receives a json on a passed socket"""
    data = b""
    while True:
        chunk = socket.recv(1024)
        if not chunk:
            break
        data += chunk

    json_data = json.loads(data.decode("utf-8"))
    print("Received JSON:", json_data)
    return json_data


def send_hello():
    """builds a hello command for and sends it to the master node"""
    hello_msg = {
        "message": cfg["authentication"]["stored_hello_message"],
        "pass": cfg["authentication"]["stored_hello_pass"],
        "ip": agentIp,
        "hostname": socket.gethostname(),
    }
    send_json(masterIp, multicastPort, hello_msg)
