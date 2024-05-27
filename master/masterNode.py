from flask import Flask, render_template, jsonify, request

from modules import asyncBeaconRoutines as asyncBeacon
from modules import dataProcessing
from modules import executionRoutines
from modules import dbAdapter
import multiprocessing as mp


app = Flask(__name__, static_folder="static/static", template_folder="static")
db_adapter = dbAdapter.SQLiteDBAdapter()


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
    # executionRoutines.startScripts(data["startParams"])
    executionRoutines.startScriptsPresetParams(data["startParams"])

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

        new_param = request.get_json()
        if not new_param or "value" not in new_param:
            return jsonify({"error": "Invalid input"}), 400
        print(new_param)
        db_adapter.insert_params_setting(new_param["value"])

        return jsonify(new_param), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/cmdParams", methods=["GET"])
def readCommandParams():
    """
    @brief: get a list of command params
    @return: json containing list of cmd params as a value for cmdParamsList key
    """

    params_list = db_adapter.get_all_params_settings()
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

        # Find the item by ID and update it
        if db_adapter.update_params_setting(item_id, updated_param["value"]):
            return jsonify(updated_param), 200

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

    try:

        if db_adapter.delete_params_setting(item_id):
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
