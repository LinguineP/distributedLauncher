# Distributed launcher for the MPT-FLA federated learning framework

This project is supposed to start MPT-FLA(MicroPython testbed for Federated Learning Algorithms) applications on remote machines (link to PTB-FLA github repository which also contains MPT-FLA as its successor https://github.com/miroslav-popovic/ptbfla)
-for the full source including the fe, switch to the dev branch

## Usage:
### main operation:
  1. Copy master node directory to the desired PC
  
  2. Copy agents to PCs that are going to run MPT-FLA applications
  
  3. Change config for masterNode and for agents according to your preference (also check that you followed along the ptb_fla instalation)
  
  4. create new masternodeDB.db file in master/dbs directory in order to start with a clean database
  
  5. start the masterNode with python (run masterNode.py)
  
  6. either click on a link provided in console or type http://yourpcslocalip:8080 into the browser
  
  7. click start discovery
  
  8. start your agents with python (run agentNode.py) --note: it may require netifaces if not installed already
  
  9. stop discovery and proceed with launch 
### launch operation:
  1. from the list of available nodes select the nodes you want to start
 
  2. long press the node you want to start first
  
  3. click the application you want to start
  
  4. click the parameters you want to use
  
  5. press launch button

### additional functionalities:
  Execution time measurement and data analysis

### Contents:

- agents - contains the agent node which is responsible for running the aplication on selected devices
- master - contains the master node which is responsible for the discovery process , control over the agent node actions, measurement, and measurement analysis
