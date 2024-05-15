import messagingHandler as msg


portComm = 5002


def startScripts(params_dict):
    # TODO implement starting of scripts
    # example params_dict{'selectedScript': None, 'selectedNumberOfNodes': 2, 'selectedNodes': [{'hostname': 'pv_t480s', 'ip': '192.168.0.24'}]}
    selectedScript = params_dict["selectedScript"]
    selectedNumberOfNodes = params_dict["selectedNumberOfNodes"]
    selectedNodes = params_dict["selectedNodes"]

    if selectedScript is None:
        return "No script selected"

    nodeNo = 0
    masterNode = []
    if msg.masterIp:
        masterNode = list(
            filter(lambda node: node["ip"] == msg.masterIp, selectedNodes)
        )
        selectedNodes = list(
            filter(lambda node: node["ip"] != msg.masterIp, selectedNodes)
        )
        msg.send_start(
            dest_ip=masterNode[0]["ip"],
            script=selectedScript,
            numberOfNodes=selectedNumberOfNodes,
            nodeId=0,
            masterNodeId=0,
            masterNodeIp=masterNode[0]["ip"],
            decent=False,
        )
        nodeNo = 1

    for node in selectedNodes:
        if nodeNo == 0:
            masterNode.append(node)
            print(f"master node will be {node['hostname']} at ip {node['ip']}")
        msg.send_start(
            dest_ip=node["ip"],
            script=selectedScript,
            numberOfNodes=selectedNumberOfNodes,
            nodeId=0,
            masterNodeId=0,
            masterNodeIp=masterNode[0]["ip"],
            decent=False,
        )
        nodeNo += 1


def shutdownAgentsGracefully(nodesAlive):
    # TODO implement shuttingdown of agents
    shutdown_msg = {"message": "shutdown_agent"}
    for node in nodesAlive:
        msg.send_json(dest_ip=node["ip"], dest_port=portComm, data_dict=shutdown_msg)
