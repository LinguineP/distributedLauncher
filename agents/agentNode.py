import sys
import agentModules.agentMessaging as msg
import agentModules.agentOps as ops

masterIpStore = {}
masterIpKey = "masterIp"


def discovery():
    master_ip = ops.connect()
    masterIpStore[masterIpKey] = master_ip


def execution():
    return ops.wait_for_instructions()


def agentProcess():

    agent_active = True
    while agent_active:
        try:
            if masterIpKey not in masterIpStore:
                discovery()

            agent_active = execution()
        except KeyboardInterrupt:
            print("Shutting down the agent...")
            exit(1)


if __name__ == "__main__":
    # platform check
    if sys.platform != "win32" and sys.platform != "linux":
        print("Error:", sys.platform, "is not supported!")
        exit(0)
    # start the main routine
    print("\n####################################################")
    print("\n################### Agent Node #####################")
    print("\n####################################################\n")

    agentProcess()
