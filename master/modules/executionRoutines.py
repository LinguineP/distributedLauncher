import time
import messagingHandler as msg
import utils


portComm = 55002


def startScripts(params_dict):
    # Extract parameters from the dictionary
    selectedScript = params_dict.get("selectedScript")
    selectedNumberOfNodes = params_dict.get("selectedNumberOfNodes")
    selectedNodes = params_dict.get("selectedNodes")
    decentFlag = params_dict.get("decentSelected")

    # Check if a script is selected
    if not selectedScript:
        return "No script selected"

    # Initialize variables
    masterNode = []
    nodeNo = 0

    # Iterate through remaining nodes
    for node in selectedNodes:
        time.sleep(0.5)

        msg.send_start(
            dest_ip=node["ip"],
            script=selectedScript,
            numberOfNodes=selectedNumberOfNodes,
            nodeId=nodeNo,
            masterNodeId=0,
            masterNodeIp=selectedNodes[0]["ip"],
            decent=decentFlag,
        )
        nodeNo += 1

    return "Scripts started successfully"


def startScriptsPreset(params):

    selectedNodes = params["selectedNodes"]
    selectedScript = params["selectedScript"]
    selectedParams: str = utils.remove_double_spaces(params["selectedParams"])
    print(selectedParams)
    masterIp = utils.extractIpfromString(selectedParams)

    paramsAsList = selectedParams.split(" ")
    masterNodeId = -1
    isitip = False  # utils.extractIpfromString(paramsAsList[2])
    print(isitip)
    if isitip:
        masterNodeId = int(paramsAsList[1])
        selectedNodes = [entry for entry in selectedNodes if entry["ip"] != masterIp[0]]
        masterParams = utils.replace_node_id(selectedParams, masterNodeId)
        msg.send_start_set_params(masterIp[0], selectedScript, masterParams)
        print("master")
        time.sleep(2.0)

    nodeCounter = 0

    for node in selectedNodes:
        if nodeCounter == masterNodeId:
            nodeCounter += 1
        nodeParams = utils.replace_node_id(selectedParams, nodeCounter)
        msg.send_start_set_params(node["ip"], selectedScript, nodeParams)
        nodeCounter += 1

    return "Scripts started successfully"


def shutdownAgentsGracefully(nodesAlive):
    # TODO implement shuttingdown of agents
    shutdown_msg = {"message": "shutdown_agent"}
    for node in nodesAlive:
        msg.send_json(dest_ip=node["ip"], dest_port=portComm, data_dict=shutdown_msg)
