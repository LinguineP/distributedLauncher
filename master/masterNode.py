import os
from flask import Flask, abort, render_template, jsonify, request, send_file
import multiprocessing as mp
from modules import asyncBeaconRoutines as asyncBeacon
from modules import executionRoutines
from modules import dataHandler
from modules.utils import change_slashes


app = Flask(__name__, static_folder="static/static", template_folder="static")


masterIp = ""
nodesAlive = []


@app.route("/api/stopScan", methods=["GET"])
def stopScan():
    global nodesAlive, beacon
    if beacon.is_alive():
        asyncBeacon.stop_beacon(stop_event=stop_event)
        nodesAlive = parent_end.recv()
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
    data = request.get_json()
    # example data {'startParams': {'selectedScript': None, 'masterIp': '192.1.1.10',selectedParams:"3 id 0 mip", 'selectedNodes': [{'hostname': 'pv_t480s', 'ip': '192.168.0.24'}]}} incoming data example
    print(data)
    executionRoutines.startScriptsPreset(data["startParams"])

    return "Success", 200


@app.route("/api/shutdownAgents", methods=["POST"])
def shudownAgents():
    data = request.get_json()
    nodesAlive = data["stopParams"]["selectedNodes"]
    executionRoutines.shutdownAgentsGracefully(nodesAlive)
    return "Success", 200


@app.route("/api/startMeasuring", methods=["POST"])
def startMeasuring():

    data = request.get_json()

    executionRoutines.startBatch(data)

    return "Success", 200


@app.route("/api/doAnalysis", methods=["POST"])
def doAnalysis():

    data = request.get_json()

    executionRoutines.doAnalysis(data)

    return "Success", 200


@app.route("/api/exportCSV", methods=["POST"])
def exportCSV():

    executionRoutines.generateCSV()

    return "Success", 200


@app.route("/api/cmdParams", methods=["POST"])
def createCommandParam():
    """
    @brief: create a new command param
    """
    try:

        data = request.get_json()
        if not data or "value" not in data:
            return jsonify({"error": "Invalid input"}), 400

        ret = dataHandler.insert_params_setting(data)

        return jsonify({"paramsList": [ret]}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/cmdParams", methods=["GET"])
def readCommandParams():
    """
    @brief: get a list of command params
    @return: json containing list of cmd params as a value for cmdParamsList key
    """

    params_list = dataHandler.get_params_settings()
    availableScripts: list = dataHandler.getAvailableScripts()

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
        data = request.get_json()
        if not data or "value" not in data:
            return jsonify({"error": "Invalid input"}), 400

        # Find the item by ID and update it
        if dataHandler.update_param(item_id, data):
            return jsonify(data), 200

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

        if dataHandler.delete_param(item_id):
            return jsonify({"message": "Item deleted"}), 200

        return jsonify({"error": "Item not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/sessions", methods=["POST"])
def createSession():
    """
    @brief: create a new session
    """
    try:

        new_session = request.get_json()
        if (
            not new_session
            or "sessionName" not in new_session
            or "sessionScript" not in new_session
        ):
            return jsonify({"error": "Invalid input"}), 400

        ret = dataHandler.insert_session(new_session)

        return jsonify([ret]), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/sessions", methods=["GET"])
def readSessions():
    """
    @brief: get a list of sessions
    @return: json containing list of sessions
    """

    sessionList = dataHandler.get_all_sesisions()

    return jsonify(sessionList)


@app.route("/api/sessions/sessionResults", methods=["GET"])
def readSessionResults():
    """
    @brief: get session results for a given session ID
    @return: json containing session results
    """
    session_id = request.args.get("sessionId")
    if not session_id:
        return jsonify({"error": "Missing sessionId parameter"}), 400

    try:
        sessionList = dataHandler.get_session_results(session_id)

        return jsonify(sessionList)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/sessions/batchResults", methods=["GET"])
def readBatchResults():
    """
    @brief: get batch results for a given session ID
    @return: json containing list of batch results
    """
    session_id = request.args.get("sessionId")
    if not session_id:
        return jsonify({"error": "Missing sessionId parameter"}), 400

    try:
        batchResults = dataHandler.get_session_batch_results(session_id)
        return jsonify(batchResults)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/measuringStatus", methods=["GET"])
def measuringStatus():

    if (
        dataHandler.check_measurement_status_exists()
        and dataHandler.check_measurement_repetition_number_exists()
    ):
        status = {
            "status": dataHandler.retrive_measurment_status(),
            "repetitionNumber": dataHandler.retrive_repetition_number(),
        }
    else:
        status = {"status": "idle", "repetitionNumber": -1}

    return jsonify(status)


@app.route("/api/imagePng/<path:filename>")
def serve_image(filename):

    filename = change_slashes(filename)

    if os.path.isfile(filename):
        return send_file(filename, mimetype="image/jpeg")
    else:
        abort(404, description="Resource not found")


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":

    print("Starting masterNode")
    app.debug = True
    app.run(host="0.0.0.0", port=8080)
