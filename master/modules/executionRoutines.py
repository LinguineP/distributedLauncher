import time
from queue import Queue
import messagingHandler as msg
import utils
import threading
import resultsGathering as rg
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


def startScriptsPreset(params, measure=False):

    selectedNodes = params["selectedNodes"]
    selectedScript = params["selectedScript"]
    masterIp = params["masterNodeIp"]

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
    if paramsAsList[2] != "mip":
        firstNodeId = paramsAsList[2]
        nodeParams = utils.replace_node_id(selectedParams, firstNodeId)
        msg.send_start_set_params(masterIp, selectedScript, nodeParams, measure)
    nodeId = 0
    # iterates over selected nodes this is ok because it allows for some nodes to be manualy started
    for node in selectedNodes:
        if nodeId == int(firstNodeId):
            nodeId += 1
            continue  # skips the node that was already started
        nodeParams = utils.replace_node_id(selectedParams, nodeId)
        msg.send_start_set_params(node["ip"], selectedScript, nodeParams, measure)
        nodeId += 1

    return "Scripts started successfully"


def shutdownAgentsGracefully(nodesAlive):
    shutdown_msg = {"message": "shutdown_agent"}
    for node in nodesAlive:
        msg.send_json(dest_ip=node["ip"], dest_port=portComm, data_dict=shutdown_msg)
