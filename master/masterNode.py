from flask import Flask, render_template,jsonify
from modules import asyncBeaconRoutines as asyncBeacon
import multiprocessing as mp
import socket

app = Flask(__name__, static_folder="static/static", template_folder="static")

masterIp=''
nodesAlive=[]

@app.route("/api/stopScan")
def stopScan():
    if  beacon.is_alive():
        asyncBeacon.stop_beacon(stop_event=stop_event)  
        asyncBeacon
        nodesAlive:list=parent_end.recv()
        response={"message": "Worker stopped.","nodes":nodesAlive}
        return jsonify(response)

@app.route("/api/startScan")
def startScan():
    global listener,beacon, stop_event,parent_end
    parent_end,child_end= mp.Pipe();
    stop_event = mp.Event()
    listener = mp.Process(target=asyncBeacon.incomingListener_process, args=(stop_event,child_end))
    beacon = mp.Process(target=asyncBeacon.beacon_process, args=(stop_event,))
    listener.start()
    beacon.start()
    return jsonify({"message": "Worker started."})


@app.route("/api/startNodes")
def startNodes():
    #TODO: issue start command
    pass
    



@app.route("/")
def index():
    #TODO: fix avail node json mappings
    return render_template('index.html')





if __name__ == "__main__":

    print('Starting masterNode')
    app.debug=True
    app.run(host='0.0.0.0',port=8080)
