import time
import utils
import agentMessaging as msg
from shellInteract import *


def run_script(script_cmd: str, measure=False):
    """runs the script specified in the cmd parameter"""
    print()
    print("\n------------------------------------------------------------\n")
    handler = ShellHandler()

    start_time = time.perf_counter()
    output, error = handler.run_command(script_cmd)
    end_time = time.perf_counter()

    execution_time = end_time - start_time

    print(error)
    print(output)

    if measure:
        msg.sendResults(output, execution_time)

    print("\n------------------------------------------------------------\n\n")


def start_node_params(script, params, measure=False):
    print("node started")
    cmd = f"{utils.get_python_cmd()} {utils.find_file(utils.escape_chars(agentConfig.cfg['baseProjectPath']),script)} {params}"
    print(cmd)
    run_script(cmd, measure)


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
    if received["message"] == "start_node_params":
        start_node_params(received["script"], received["params"], received["measure"])
        received = None
    elif received["message"] == "shutdown_agent":
        exit_gracefully()
        return False
    elif received["message"] == "alive_ping":
        pass
    else:
        print("Unknown command")

    return True
