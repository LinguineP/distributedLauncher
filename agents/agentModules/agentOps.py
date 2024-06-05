import time
import utils
import agentMessaging as msg
from shellInteract import *


def run_script(script_cmd: str):
    """runs the script specified in the cmd parameter"""
    print()
    print("\n------------------------------------------------------------\n")
    handler = ShellHandler()

    handler.run_command(script_cmd)

    print("\n------------------------------------------------------------\n\n")


def decent_cmd_builder(script, numberOfNodes, currentNodeId, masterNodeIp) -> str:
    """decentralised FL command builder"""

    runDecentCmd = (
        f"{utils.get_python_cmd()}"
        f" "
        f"{utils.find_file( utils.escape_chars(agentConfig.cfg['baseProjectPath']),script)}"
        f" "
        f"{numberOfNodes}"
        f" "
        f"{currentNodeId}"
        f" "
        f"{masterNodeIp}"
    )

    return runDecentCmd


def cent_cmd_builder(
    script, numberOfNodes, currentNodeId, masterNodeId, masterNodeIp
) -> str:
    """decentralised FL command builder"""

    runCentCmd = (
        f"{utils.get_python_cmd()}"
        f" "
        f"{utils.find_file( utils.escape_chars(agentConfig.cfg['baseProjectPath']),script)}"
        f" "
        f"{numberOfNodes}"
        f" "
        f"{currentNodeId}"
        f" "
        f"{masterNodeId}"
        f" "
        f"{masterNodeIp}"
    )

    return runCentCmd


def start_node(
    script, numberOfNodes, currentNodeId, masterNodeId, masterNodeIp, decent
):
    print("node started")
    print(script, numberOfNodes, masterNodeId, currentNodeId, masterNodeIp, decent)
    cmd = ""
    if decent:
        cmd = decent_cmd_builder(script, numberOfNodes, currentNodeId, masterNodeIp)
    else:
        cmd = cent_cmd_builder(
            script, numberOfNodes, currentNodeId, masterNodeId, masterNodeIp
        )

    run_script(cmd)


def start_node_params(script, params):
    print("node started")
    cmd = f"{utils.get_python_cmd()} {utils.find_file(utils.escape_chars(agentConfig.cfg['baseProjectPath']),script)} {params}"
    print(cmd)
    run_script(cmd)


def connect() -> str:
    masterIp = msg.receive_ip_from_multicast()
    msg.send_hello()
    return masterIp


def exit_gracefully():
    """cleans up before a gracefull exit"""

    print("Shutting down the agent...")


def wait_for_instructions():
    """reacts to commands sent to agent from server"""

    global _shell_active

    received = msg.receive_command()
    if received["message"] == "start_node":
        start_node(
            received["script"],
            received["numberOfNodes"],
            received["currentNodeId"],
            received["masterNodeId"],
            received["masterNodeIp"],
            received["decent"],
        )
        received = None
    elif received["message"] == "start_node_params":
        start_node_params(received["script"], received["params"])
        received = None
    elif received["message"] == "shutdown_agent":
        exit_gracefully()
        return False
    elif received["message"] == "alive_ping":
        pass
    else:
        print("Unknown command")

    return True


if __name__ == "__main__":
    run_script(
        "python D:\\fax\\diplomski\\ptbfla2.0\src\examples\mp_async_example2_cent_avg.py 1 0 0 192.168.1.165"
    )
