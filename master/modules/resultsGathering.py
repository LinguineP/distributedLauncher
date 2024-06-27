import socket
import threading
import queue
import json
import dbAdapter


db_adapter = dbAdapter.SQLiteDBAdapter()

data_passer: dbAdapter.SQLiteDBAdapter.DataPasser = (
    dbAdapter.SQLiteDBAdapter().dataPasser
)


def ingest_result(message):
    global data_passer, db_adapter

    answerCounter = int(data_passer.retrieve("answerCounter"))
    currentRunId = data_passer.retrieve("currentRunId")
    nodeId = db_adapter.nodes.get_node_id(message["hostname"], message["ip"])
    db_adapter.node_data.create_node_data(
        currentRunId, nodeId, message["runOutput"], message["runTime"]
    )
    data_passer.store("answerCounter", answerCounter + 1)


def process_queue_messages(message_queue, stop_event):
    while not stop_event.is_set():
        try:
            message = message_queue.get(timeout=0.5)
            ingest_result(message)
            message_queue.task_done()
        except queue.Empty:
            continue


def handle_client_connection(client_socket, message_queue, stop_event):
    while not stop_event.is_set() or not message_queue.empty():
        data = client_socket.recv(1024)
        if data:
            message = data.decode("utf-8")
            try:
                json_message = json.loads(message)
                message_queue.put(json_message)
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON message: {e}")
        else:
            print("Client disconnected")
            break
    client_socket.close()


def results_listener(host, port, numberOfexpectedClis, stop_event, message_queue):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if host == None:
        print("Invalid host IP address")
        return
    server_socket.bind((host, port))

    server_socket.listen(numberOfexpectedClis)

    threads = []
    while not stop_event.is_set():
        try:
            # Wait for a connection
            server_socket.settimeout(30)
            client_socket, client_address = server_socket.accept()

            # Start a new thread to handle the client connection
            client_thread = threading.Thread(
                target=handle_client_connection,
                args=(client_socket, message_queue, stop_event),
            )
            client_thread.daemon = True
            client_thread.start()
            threads.append(client_thread)
        except socket.timeout:
            continue

    # Wait for all client threads to finish
    for t in threads:
        t.join()

    server_socket.close()
    print("Server stopped")


def stop_server(stop_event):
    input("Press Enter to stop the server...\n")
    stop_event.set()
