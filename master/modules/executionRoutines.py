import time
import messagingHandler as msg
import utils


portComm = 55002


def startScriptsPreset(params):

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
        msg.send_start_set_params(masterIp, selectedScript, nodeParams)
    nodeId = 0
    # iterates over selected nodes this is ok because it allows for some nodes to be manualy started
    for node in selectedNodes:
        if nodeId == int(firstNodeId):
            nodeId += 1
            continue  # skips the node that was already started
        nodeParams = utils.replace_node_id(selectedParams, nodeId)
        msg.send_start_set_params(node["ip"], selectedScript, nodeParams)
        nodeId += 1

    return "Scripts started successfully"


def shutdownAgentsGracefully(nodesAlive):
    shutdown_msg = {"message": "shutdown_agent"}
    for node in nodesAlive:
        msg.send_json(dest_ip=node["ip"], dest_port=portComm, data_dict=shutdown_msg)
