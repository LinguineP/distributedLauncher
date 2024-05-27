from flask import Flask, render_template, jsonify, request

from modules import asyncBeaconRoutines as asyncBeacon
from modules import dataProcessing
from modules import executionRoutines

import multiprocessing as mp
import socket

app = Flask(__name__, static_folder="static/static", template_folder="static")


masterIp = ""
nodesAlive = []


@app.route("/api/stopScan", methods=["GET"])
def stopScan():
    global nodesAlive, beacon
    if beacon.is_alive():
        asyncBeacon.stop_beacon(stop_event=stop_event)
        nodesAlive = parent_end.recv()
        availableScripts: list = dataProcessing.getAvailableScripts()
        response = {
            "message": "Worker stopped.",
            "availableNodes": nodesAlive,
        }

        return jsonify(response)


@app.route("/api/startScan", methods=["GET"])
def startScan():
    global listener, beacon, stop_event, parent_end
    parent_end, child_end = mp.Pipe()
    stop_event = mp.Event()
    listener = mp.Process(
        target=asyncBeacon.incomingListener_process, args=(stop_event, child_end)
    )
    beacon = mp.Process(target=asyncBeacon.beacon_process, args=(stop_event,))
    listener.start()
    beacon.start()
    return jsonify({"message": "Worker started."})


@app.route("/api/startNodes", methods=["POST"])
def startNodes():
    # TODO: issue start command
    data = request.get_json()
    # example data {'startParams': {'selectedScript': None, 'selectedNumberOfNodes': 2, 'selectedNodes': [{'hostname': 'pv_t480s', 'ip': '192.168.0.24'}]}} incoming data example
    executionRoutines.startScripts(data["startParams"])

    return "Success", 200


@app.route("/api/shutdownAgents", methods=["POST"])
def shudownAgents():
    # TODO : add node stopping to frontend look at app.js todos
    data = request.get_json()
    nodesAlive = data["stopParams"]["selectedNodes"]
    executionRoutines.shutdownAgentsGracefully(nodesAlive)
    return "Success", 200


@app.route("/api/cmdParams", methods=["POST"])
def createCommandParam():
    """
    @brief: create a new command param
    """
    try:
        params_list = []
        # Parse the incoming JSON request body
        new_param = request.get_json()
        if not new_param or "value" not in new_param:
            return jsonify({"error": "Invalid input"}), 400

        # Create a new id for the new parameter
        new_id = max(param["id"] for param in params_list) + 1 if params_list else 1
        new_param["id"] = new_id

        # Add the new parameter to the data store
        params_list.append(new_param)

        # Return the created parameter and a 201 status code
        return jsonify(new_param), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/cmdParams", methods=["GET"])
def readCommandParams():
    """
    @brief: get a list of command params
    @return: json containing list of cmd params as a value for cmdParamsList key
    """

    params_list = [
        {"id": 1, "value": "Item 1"},
        {"id": 2, "value": "Item 2"},
        {"id": 3, "value": "Item 3"},
    ]
    availableScripts: list = dataProcessing.getAvailableScripts()

    return jsonify({"paramsList": params_list, "availableScripts": availableScripts})


@app.route("/api/cmdParams/<int:item_id>", methods=["PUT"])
def updateCommandParams(item_id):
    """
    @brief: update one of the command param with the given item_id
    @param: id of the item to be updated
    @return: update status
    """
    try:
        # Parse the incoming JSON request body
        updated_param = request.get_json()
        if not updated_param or "value" not in updated_param:
            return jsonify({"error": "Invalid input"}), 400
        params_list = [
            {"id": 1, "value": "Item 1"},
            {"id": 2, "value": "Item 2"},
            {"id": 3, "value": "Item 3"},
        ]
        # Find the item by ID and update it
        for param in params_list:
            if param["id"] == item_id:
                param["value"] = updated_param["value"]
                return jsonify(param), 200

        return jsonify({"error": "Item not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/cmdParams/<int:item_id>", methods=["DELETE"])
def deleteCommandParam(item_id):
    """
    @brief: delete one of the command params with the given item_id
    @param: id of the item to be deleted
    @return: delete status
    """
    params_list = [
        {"id": 1, "value": "Item 1"},
        {"id": 2, "value": "Item 2"},
        {"id": 3, "value": "Item 3"},
    ]
    try:
        # Find the item by ID and delete it
        for param in params_list:
            if param["id"] == item_id:
                params_list.remove(param)
                return jsonify({"message": "Item deleted"}), 200

        return jsonify({"error": "Item not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# TODO: define cent decent choice in fe,currently hardcoded do docsstrings for masternode
@app.route("/")
def index():
    return render_template("index.html")


# TODO: implement some kind of encription and probably digital signitures
if __name__ == "__main__":

    print("Starting masterNode")
    app.debug = True
    app.run(host="0.0.0.0", port=8080)
