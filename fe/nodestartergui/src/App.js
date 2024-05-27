import './App.css';
import React, { useState, useEffect, useMemo } from 'react';
import RunnableNodeList from './runnablenodeList/RunnableNodeListComponent';
import CommandParamsList from './paramsList/CommandParamsList.jsx';
import CommunicationHandler from './communicationHandlers/communicationHandler.ts';

function App() {
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
        const data = await requestHandler.getCmdParams();
        console.log(data.paramsList)
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

  return (
    <div className="App">
      <header className="App-header">
        <p className='buttonText'>Welcome to distributed app starter</p>

        <button onClick={discovery} className="Action-button">
          <p className='Button-text'>{discoveryOn ? stopDiscoveryText : startDiscoveryText}</p>
        </button>

        <div className="selectionOutline">
          <div className="halfDiv">
            <p>Available Nodes</p>
            <hr></hr>
            <RunnableNodeList items={availableNodes} script={false} onItemClick={itemWasClickedAvailable} />
          </div>
          <div className="halfDiv">
            <p>Selected Nodes</p>
            <hr></hr>
            <RunnableNodeList items={selectedNodes} script={false} onItemClick={itemWasClickedSelected} />
          </div>
        </div>

        <div className="wideOutline">
          <p>Available Scripts</p>
          <hr></hr>
          <RunnableNodeList items={availableScripts} script={true} onItemClick={itemWasClickedScript} lastClickedScript={lastClickedScript} setLastClickedScript={setLastClickedScript} />
        </div>

        <div className="wideOutline">
          <div className="selectionOutline">
            <CommandParamsList paramsList={paramsList}
            itemClicked={(value)=>{setLastClickedParamsText(value) }} />
          </div>
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
      </header>
    </div>
  );
}

export default App;
