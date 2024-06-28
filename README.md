# Distributed launcher

This project is supposed to start MPT-FLA(MicroPython testbed for Federated Learning Algorithms) aplications on remote machines (link to PTB-FLA github repository which also contains MPT-FLA as its successor https://github.com/miroslav-popovic/ptbfla )

## Usage:
### main operation:
  1. Copy master node directory to the desired PC
  
  2. Copy agents to PCs that are going to run MPT-FLA applications
  
  3. Change config for masterNode and for agents according to your preference (also check that you followed along the ptb_fla instalation)
  
  4. create new masternodeDB.db file in master/dbs directory in order to start with a clean database
  
  5. start the masterNode with python (run masterNode.py)
  
  6. either click on a link provided in console or type http://<yourpcslocalip>:8080 into the browser
  
  7. click start discovery
  
  8. start your agents with python (run agentNode.py) --note: it may require netifaces if not installed already
  
  9. stop discovery and proceed with launch 
### launch operation:
  1. from the list of available nodes select the nodes you want to start
 
  2. long press the node you want to start first
  
  3. click the application you want to start
  
  4. click the parameters you want to use
  
  5. press launch button


### Contents:

- agents - contains the agent node which is responsible for running the scripts on selected devices
- fe - contains the frontend code for the destributed launcher which is built and placed into the master/static dir via the buildUtil.py script
- master - contains the master node which is responsible for the discovery process , control over the agent node actions
