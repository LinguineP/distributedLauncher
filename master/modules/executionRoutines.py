import time
import messagingHandler as msg


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
    pass


def shutdownAgentsGracefully(nodesAlive):
    # TODO implement shuttingdown of agents
    shutdown_msg = {"message": "shutdown_agent"}
    for node in nodesAlive:
        msg.send_json(dest_ip=node["ip"], dest_port=portComm, data_dict=shutdown_msg)
