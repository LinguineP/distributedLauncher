import json
import socket
from agentConfig import *
import socket

multicastGroup = '239.255.0.0'
portMulticast = 55001 #not a known port number
portComm=55002
masterIp=''


agentIp = ''



def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.255.255.255', portMulticast))  # the address 10.255.255.255 is from the Private IP Address Range
        local_ip = s.getsockname()[0]
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        return local_ip
    except Exception as e:
        print("Error:", e)
        return None

def receive_ip_from_multicast():
    global masterIp,agentIp

    agentIp=get_local_ip()
    multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    multicast_socket.bind(('', portMulticast)) 
    multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 3) #sets ttl 3 hops seemed reasonable for a local network
    multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(multicastGroup) + socket.inet_aton('0.0.0.0'))
    
    #print(f"Waiting to receive IP address from multicast group {multicast_group} on port {port}")
    
    while True:
        data, _ = multicast_socket.recvfrom(1024)
        if data:
            masterIp=data.decode('utf-8')
            print(f"Received IP address: {masterIp}")
            return masterIp


def server_ping():
    pass





def send_json(dest_ip, dest_port, data_dict):
    # Convert the dictionary to JSON
    json_data = json.dumps(data_dict)
    
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to the server
        print(dest_ip,dest_port)
        client_socket.connect((dest_ip, dest_port))
        print("Connected to server.")
        
        # Send the JSON data
        client_socket.sendall(json_data.encode("utf-8"))
        print("JSON data sent successfully.")
    finally:
        client_socket.close()



def receive_command():
    agent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    agent_socket.bind((masterIp, portComm))
    agent_socket.listen(1)

    try:
        master_socket, master_address = agent_socket.accept()

        json_data=receive_json(master_socket)
        print("Received JSON:", json_data)
        return json_data
    except Exception as e:
        #print("Error:", e)
        pass
    finally:
        agent_socket.close()

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


def send_hello():
    hello_msg={"message":cfg['authentication']['stored_hello_message'],
                "pass":cfg['authentication']['stored_hello_pass'],
                "ip":agentIp,
                "hostname":socket.gethostname()}
    send_json(masterIp,portComm,hello_msg)