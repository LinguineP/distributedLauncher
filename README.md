# Distributed launcher 

This project is supposed to start set processes on remote machines (ie. pyhton scripts)


## Usage:
  1) start master node and open the web app
  2) start agentNodes

### Contents:
  agents - contains the agent node which is responsible for running the scripts on selected devices
  fe - contains the frontend code for the destributed launcher which is built and placed into the master/static dir via the buildUtil.py script
  master - contains the master node which is responsible for the discovery process , control over the agent node actions (#TODO: file distribution, result gathering)
