import '../App.css';
import React, { useState, useEffect, useMemo } from 'react';
import AvailableNodesList from '../components/runnablenodeList/AvailableNodesListComponent.jsx';
import SelectedNodesList from '../components/runnablenodeList/SelectedNodesListComponent.jsx';
import AvailableScriptsList from '../components/availableScriptsList/AvailableScriptsListComponent.jsx';
import CommandParamsList from '../components/paramsList/CommandParamsList.jsx';
import CommunicationHandler from '../services/communicationHandlers/communicationHandler.ts';
import DataVault from '../services/dataVault.ts'

function LauncherPanel() {
  
  const requestHandler = useMemo(() => {
    return new CommunicationHandler();
  }, []);

  const [discoveryOn, setDiscoveryOn] = useState(false);
  const startDiscoveryText = "Start discovery";
  const stopDiscoveryText = "Stop discovery";

  const [paramsList, setParamsList] = useState([]);

  useEffect(() => {
    const getParamsList = async () => {
      try {
        const dataVault = DataVault.getInstance();
        let data
        if(dataVault.getDirty("paramsList")){
          data= await requestHandler.getCmdParams();
        }
        else{
          data={'paramsList':dataVault.getItem("paramsList"),"availableScripts":dataVault.getItem("availableScripts")}
        }

        
        setParamsList(data.paramsList);
        setAvailableScripts(data.availableScripts);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    }

    getParamsList();
  }, [requestHandler]);

  const [availableNodes, setAvailableNodes] = useState([]);
  const [selectedNodes, setSelectedNodes] = useState([]);
  const [availableScripts, setAvailableScripts] = useState([]);
  const [lastClickedScriptText, setLastClickedScriptText] = useState("");
  const [lastClickedParamsText, setLastClickedParamsText] = useState(""); 
  

  const discovery = async () => {
    setDiscoveryOn(!discoveryOn);
    if (!discoveryOn) {
      requestHandler.startScan();
      return;
    }
    const response = await requestHandler.stopScan();
    setAvailableNodes(response.availableNodes);
  };

  

  const startRemote = async () => {
    console.log(lastClickedScriptText);
    
    
    const requestParams = {
      selectedScript: lastClickedScriptText, // Use the text content of the last clicked script
      selectedParams: lastClickedParamsText, // Use the text content of the last clicked params
      selectedNodes: selectedNodes,
      masterNodeIp: longPressedItem.ip
    }
    requestHandler.startNodes(requestParams);
  };

  const stopRemote = async () => {
    const requestParams = {
      selectedNodes: selectedNodes
    }
    requestHandler.stopNodes(requestParams);
  };

  const itemWasClickedAvailable = (item) => {
    const updatedAvailableNodes = availableNodes.filter((listItem) => listItem !== item);
    setAvailableNodes(updatedAvailableNodes);
    setSelectedNodes([...selectedNodes, item]);
  };

  const itemWasClickedSelected = (item) => {
    const updatedSelectedNodes = selectedNodes.filter((listItem) => listItem !== item);
    setAvailableNodes([...availableNodes, item]);
    setSelectedNodes(updatedSelectedNodes);
  };

  const [lastClickedScript, setLastClickedScript] = useState(null);

  const itemWasClickedScript = (item) => {
    setLastClickedScript(item);
    setLastClickedScriptText(item); // Set the text content of the last clicked item
  };


  const [numberOfSelectedNodes, setNumberOfSelectedNodes] = useState(selectedNodes.length);

   const updateSelectedCount = (count) => {
    setNumberOfSelectedNodes(count);
  };

  const [longPressedItem, setLongPressedItem] = useState(null);
  const handleItemLongPress = (item) => {
    setLongPressedItem(item);
    console.log('Item long-pressed:', item);
  };

  return (
    <div className="App">
      <header className="App-header">
            <div className='panelHeader'>
                  <div className='sessionBody'>
                    <p className='buttonText'>Welcome to distributed Launcher</p>
                    <button onClick={discovery} className="Action-button">
                      <p className='Button-text'>{discoveryOn ? stopDiscoveryText : startDiscoveryText}</p>
                    </button>
                    <div className='line'>
                                <hr />
                    </div>

                    <div className="selectionOutline">
                      <div className="halfDiv">
                        <div className='row'>
                        <p>Available Nodes</p>
                        </div>
                        <hr></hr>
                        <AvailableNodesList items={availableNodes}  onItemClick={itemWasClickedAvailable} />
                      </div>
                      <div className="halfDiv">
                        <div className='row'>
                        <p>Selected Nodes</p>
                        <p>{numberOfSelectedNodes}</p>
                        </div>
                        <hr></hr>
                        <SelectedNodesList items={selectedNodes}  onItemClick={itemWasClickedSelected} updateSelectedCount={updateSelectedCount} onItemLongPress={handleItemLongPress}/>
                      </div>
                    </div>

                    <div className="wideOutline">
                      <div className='row'>
                      <p>Available Scripts</p>
                      </div>
                      <hr></hr>
                      <AvailableScriptsList items={availableScripts}  onItemClick={itemWasClickedScript} lastClickedScript={lastClickedScript} setLastClickedScript={setLastClickedScript} />
                    </div>

                    <div className="wideOutline">
                      <div className="selectionOutline">
                        <CommandParamsList paramsList={paramsList}
                        itemClicked={(value)=>{setLastClickedParamsText(value) }} />
                      </div>
                    </div>
                    <div className='line'>
                                <hr />
                    </div>
                    <div className="selectionOutline">
                      <div className="altHalfDiv">
                        <div className='buttonContainer'>
                          <button onClick={startRemote}><p className='Button-text'>Start Scripts</p></button>
                        </div>
                      </div>
                      <div className="altHalfDiv">
                        <div className='buttonContainer'>
                          <button onClick={stopRemote}><p className='Button-text'>Shutdown Nodes</p></button>
                        </div>
                      </div>
                    </div>
                  </div>
            </div>
      </header>
    </div>
  );
}

export default LauncherPanel;
