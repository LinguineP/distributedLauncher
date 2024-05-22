import socket
import json


multicastGroup = "239.255.10.1"  # reserved range for local assignment by IANA
portMulticast = 55001  # not a known port number
portComm = 55002  # separate port for direct communication
connectionTimeout = 0.5
masterIp = ""


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(
            ("10.255.255.255", portMulticast)
        )  # the address 10.255.255.255 is from the Private IP Address Range
        local_ip = s.getsockname()[0]
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        return local_ip
    except Exception as e:
        print("Error:", e)
        return None


def send_ip_to_multicast():
    global portMulticast, masterIp
    masterIp = get_local_ip()
    message = masterIp.encode("utf-8")
    multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

    multicast_socket.sendto(message, (multicastGroup, portMulticast))
    multicast_socket.close()


def receive_discovery():
    global masterIp
    master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    master_socket.bind((masterIp, portMulticast))
    master_socket.listen(1)

    try:
        master_socket.settimeout(
            connectionTimeout
        )  # Set a timeout for accept() polling because accept is blocking
        # this handles that there are no new connections after the discovry has been stopped
        agent_socket, agent_address = master_socket.accept()

        json_data = receive_json(agent_socket)
        print("Received JSON:", json_data)
        return json_data
    except Exception as e:
        # print("Error:", e)
        pass
    finally:
        master_socket.close()


def receive_json(socket):
    data = b""
    while True:
        chunk = socket.recv(1024)
        if not chunk:
            break
        data += chunk

    json_data = json.loads(data.decode("utf-8"))
    print("Received JSON:", json_data)
    return json_data


def send_start(
    dest_ip, script, numberOfNodes, nodeId, masterNodeId, masterNodeIp, decent
):
    message = {
        "message": "start_node",
        "script": script,
        "numberOfNodes": numberOfNodes,
        "currentNodeId": nodeId,
        "masterNodeId": masterNodeId,
        "masterNodeIp": masterNodeIp,
        "decent": decent,
    }
    print(message)
    send_json(dest_ip, portComm, message)


def send_json(dest_ip, dest_port, data_dict):
    # Convert the dictionary to JSON
    json_data = json.dumps(data_dict)

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to the server
        client_socket.connect((dest_ip, dest_port))

        # Send the JSON data
        client_socket.sendall(json_data.encode("utf-8"))
        print("JSON data sent successfully.")
    finally:
        client_socket.close()
