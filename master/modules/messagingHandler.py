import socket
import json


multicastGroup = '224.1.1.1' # not in  the reserved range 
portMulticast = 5001 #not a known port number
portComm=5002  #separate port for direct communication 
connectionTimeout=0.5
masterIp = ''


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

def send_ip_to_multicast():
    masterIp=get_local_ip();
    message = masterIp.encode('utf-8')
    multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 3)
    multicast_socket.sendto(message, (multicastGroup, portMulticast))
    multicast_socket.close()    

def receive_discovery():
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((masterIp, portComm))
    server_socket.listen(1)

    try:
        server_socket.settimeout(connectionTimeout) # Set a timeout for accept() polling because accept is blocking
                                                    #this handles that there are no new connections after the discovry has been stopped
        client_socket, client_address = server_socket.accept()

        json_data=receive_json(client_socket)
        print("Received JSON:", json_data)
        return json_data
    except Exception as e:
        #print("Error:", e)
        pass
    finally:
        server_socket.close()


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
        
    