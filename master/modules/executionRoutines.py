import time
from queue import Queue
import threading
import utils
import messagingHandler as msg
import resultsGathering as rg
import dataAnalysis as da
import dbAdapter


db_adapter = dbAdapter.SQLiteDBAdapter()

data_passer: dbAdapter.SQLiteDBAdapter.DataPasser = (
    dbAdapter.SQLiteDBAdapter().dataPasser
)


portComm = 55002


def startRepetition(params, runNumber):

    currentBatchId = data_passer.retrieve("currentBatchId")

    runId = db_adapter.runs.create_new_run(currentBatchId, runNumber)

    data_passer.store("repetitionNumber", runNumber)

    data_passer.store("answerCounter", 1)

    data_passer.store("currentRunId", runId)

    stop_event = threading.Event()

    message_queue = Queue()

    startScriptsPreset(params, measure=True)

    numberOfNodes = int(data_passer.retrieve("numberOfNodes"))

    listener_thread = threading.Thread(
        target=rg.results_listener,
        args=(msg.masterIp, msg.portResults, numberOfNodes, stop_event, message_queue),
    )
    listener_thread.start()

    processor_thread = threading.Thread(
        target=rg.process_queue_messages, args=(message_queue, stop_event)
    )
    processor_thread.start()

    # while number of incoming messages is < number of nodes being started do some polling to check
    while numberOfNodes > int(data_passer.retrieve("answerCounter")):
        time.sleep(0.2)

    stop_event.set()
    listener_thread.join()
    processor_thread.join()


def startBatch(params):

    # initialize batch
    # store it
    numberOfNodes = len(params["selectedNodes"])

    currentBatchId = db_adapter.batches.create_new_batch(
        params["sessionId"], params["selectedParams"], numberOfNodes
    )

    data_passer.store("numberOfNodes", numberOfNodes)

    data_passer.store("currentBatchId", currentBatchId)

    data_passer.store("status", "measuring")

    numberOfReps = params["repetitionsNumber"]

    for repetition in range(1, numberOfReps + 1):
        # starts a single measurment run
        startRepetition(params, repetition)

    data_passer.store("status", "idle")

    return


def doAnalysis(params):
    sessionId, sessionName = params["session_id"], params["session_name"]
    da.do_analysis(sessionId, sessionName)


def generateCSV():
    da.generate_csv_from_combined_data()


def startScriptsPreset(params, measure=False):
    try:
        selectedNodes = params["selectedNodes"]
        selectedScript = params["selectedScript"]
        masterIp = params["masterNodeIp"]

        paramsAsList = params["selectedParams"].split(" ")

        mipFlag = paramsAsList[2] == "mip"

        stringTransforms = [
            (utils.remove_double_space, "  "),
            (utils.replace_mip, masterIp),
        ]

        selectedParams = utils.string_transformer(
            params["selectedParams"], stringTransforms
        )

        print(selectedParams)
        paramsAsList = selectedParams.split(" ")
        NumberOfNodes = paramsAsList[0]
        firstNodeId = 0
        firstNodeIp = ""
        if mipFlag:
            firstNodeId = int(paramsAsList[2])
        nodeParams = utils.replace_node_id(selectedParams, firstNodeId)
        msg.send_start_set_params(masterIp, selectedScript, nodeParams, measure)
        time.sleep(0.5)
        nodeId = 0
        # iterates over selected nodes this is ok because it allows for some nodes to be manualy started
        for node in selectedNodes:
            if nodeId == firstNodeId:
                nodeId += 1  # skips the node number of the node that was first started
            if node["ip"] == masterIp:
                print("first node", node)
                continue  # skips the node that was already started
            nodeParams = utils.replace_node_id(selectedParams, nodeId)
            msg.send_start_set_params(node["ip"], selectedScript, nodeParams, measure)
            time.sleep(0.2)
            nodeId += 1

        return False, "Scripts started successfully"
    except:
        return True, "An error occured please check params and server logs if possible"


def shutdownAgentsGracefully(nodesAlive):
    shutdown_msg = {"message": "shutdown_agent"}
    for node in nodesAlive:
        msg.send_json(dest_ip=node["ip"], dest_port=portComm, data_dict=shutdown_msg)
