from flask import Flask, render_template,jsonify, request

from modules import asyncBeaconRoutines as asyncBeacon
from modules import dataProcessing
from modules import executionRoutines

import multiprocessing as mp
import socket

app = Flask(__name__, static_folder="static/static", template_folder="static")


masterIp=''
nodesAlive=[]

@app.route("/api/stopScan",methods=['GET'])
def stopScan():
    global nodesAlive
    if  beacon.is_alive():
        asyncBeacon.stop_beacon(stop_event=stop_event)  
        nodesAlive=parent_end.recv()
        availableScripts:list=dataProcessing.getAvailableScripts()
        response={"message": "Worker stopped.","availableNodes":nodesAlive ,"availableScripts":availableScripts}

        return jsonify(response)

@app.route("/api/startScan",methods=['GET'])
def startScan():
    global listener,beacon, stop_event,parent_end
    parent_end,child_end= mp.Pipe();
    stop_event = mp.Event()
    listener = mp.Process(target=asyncBeacon.incomingListener_process, args=(stop_event,child_end))
    beacon = mp.Process(target=asyncBeacon.beacon_process, args=(stop_event,))
    listener.start()
    beacon.start()
    return jsonify({"message": "Worker started."})


@app.route("/api/startNodes",methods=['POST'])
def startNodes():
    #TODO: issue start command
    data = request.get_json()
    #example data {'startParams': {'selectedScript': None, 'selectedNumberOfNodes': 2, 'selectedNodes': [{'hostname': 'pv_t480s', 'ip': '192.168.0.24'}]}} incoming data example
    executionRoutines.startScripts(data['startParams'])
    
    return 'Success', 200
    

@app.route("/api/shutdownAgents")
def shudownAgents():
    #TODO : add node stopping to frontend look at app.js todos
    executionRoutines.shutdownAgentsGracefully(nodesAlive)


@app.route("/")
def index():
    return render_template('index.html')





if __name__ == "__main__":

    print('Starting masterNode')
    app.debug=True
    app.run(host='0.0.0.0',port=8080)
