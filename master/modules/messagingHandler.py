import socket
import json
import dbAdapter
import time
from config import cfg


data_passer: dbAdapter.SQLiteDBAdapter.DataPasser = (
    dbAdapter.SQLiteDBAdapter().dataPasser
)


multicastGroup = "239.255.10.1"  # reserved range for local assignment by IANA
portMulticast = 55001  # not a known port number
portComm = 55002  # separate port for direct communication
portResults = 55003  # separate port for results gathering
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
    data_passer.store("masterIp", masterIp)
    message = masterIp.encode("utf-8")
    multicast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    multicast_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, cfg["TTL"])

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


def send_start_set_params(dest_ip, script, params, measure):
    message = {
        "message": "start_node_params",
        "script": script,
        "params": params,
        "measure": measure,
    }
    print("here" + str(message))
    send_json(dest_ip, portComm, message)  # TODO:uncomment this


def send_json(dest_ip, dest_port, data_dict, delay=1):
    json_data = json.dumps(data_dict)

    while True:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((dest_ip, dest_port))
            client_socket.sendall(json_data.encode("utf-8"))
            print("JSON data sent successfully.")
            return  # Exit the function after a successful send
        except ConnectionRefusedError as e:
            print(f"Connection to {dest_ip}:{dest_port} refused: {e}")
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)  # Wait for the specified delay before retrying
        finally:
            client_socket.close()
