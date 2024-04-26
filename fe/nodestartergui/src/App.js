import './App.css';
import { React, useState } from 'react';
import RunnableNodeList from './runnablenodeList/RunnableNodeListComponent';
import runnableNode from './models/runnableNode.ts';
import CommunicationHandler from './communicationHandlers/communicationHandler.ts'


function App() {
  
  const requestHandler=new CommunicationHandler();

  const [discoveryOn, setDiscoveryOn] = useState(false);
  const startDiscoveryText="Start discovery";
  const stopDiscoveryText="Stop discovery";
  

  const [availableNodes,setAvailableNodes]=useState([new runnableNode("192.156.1.10",1,"this pc0"),
  new runnableNode("192.156.1.11",2,"this pc1"),
  new runnableNode("192.156.1.12",3,"this pc2")]);
  const [selectedNodes,setSelectedNodes]=useState([]);

  var selectedScript="";

  const [availableScripts,setAvailableScripts]=useState([])
  

  const discovery=async()=>{
    setDiscoveryOn(!discoveryOn)
    if(!discoveryOn){
      console.log(false)
      requestHandler.startScan();
      return
    }
    const response=requestHandler.stopScan();
    setAvailableNodes(response.availableNodes);
    setAvailableScripts(response.availableScripts);
    console.log(true)
  };
  
  const startRemote=async()=>{
    
    if (inputValue.trim() !== '') {
      setNumber(parseInt(inputValue));
      setInputValue('');
    }
    const requestParams={
                          selectedScript:selectedScript,
                          selectedNumberOfNodes:number,
                          selectedNodes:selectedNodes  
                        }
    requestHandler.startNodes(requestParams);
                
  };

    const itemWasClickedAvailable = (item) => {
    console.log(`Item with hostName ${item.hostName} and IP ${item.ip} was clicked`);
    
    const updatedAvailableNodes = availableNodes.filter((listItem) => listItem !== item);
    setAvailableNodes(updatedAvailableNodes);

    setSelectedNodes([...selectedNodes, item]);
    

    console.log(availableNodes);
  };

  const itemWasClickedSelected = (item) => {
    console.log(`Item with hostName ${item.hostName} and IP ${item.ip} was clicked`);
    const updatedSelectedNodes = selectedNodes.filter((listItem) => listItem !== item);
    setAvailableNodes([...availableNodes, item]); // Change this line
    
    // Add the item to the destination list
    setSelectedNodes(updatedSelectedNodes);

    console.log(selectedNodes);
  };
  

  const itemWasClickedScript=(item)=>{
    selectedScript=item.ScriptName;
  }

  const [number, setNumber] = useState(null);
  const [inputValue, setInputValue] = useState('');

  const handleChange = (e) => {
    setInputValue(e.target.value);
  };

  

  return (
    <div className="App">
      <header className="App-header">
       <p className='buttonText'>Welcome to script starter</p>
       <button onClick={discovery} className="Action-button"><p className='Button-text'>{discoveryOn ? stopDiscoveryText : startDiscoveryText}</p></button>
       
       <div className="selectionOutline">
        <div className="halfDiv">
          <p>Available Nodes</p>
          <hr></hr>
          <RunnableNodeList items={availableNodes} onItemClick={itemWasClickedAvailable}>

          </RunnableNodeList>
        </div>
        <div className="halfDiv">
          <p>Selected Nodes</p>
          <hr></hr>
          <RunnableNodeList items={selectedNodes} onItemClick={itemWasClickedSelected}>
          </RunnableNodeList>
        </div>
       </div>
       <div className="availableScripts">
        
          <p>Available Nodes</p>
          <hr></hr>
          <RunnableNodeList items={availableScripts} onItemClick={itemWasClickedScript}>

          </RunnableNodeList>      
       </div>
          <div className="selectionOutline">
            <div className="altHalfDiv">
            <label>
              Enter number of nodes:
              <input
                type="number"
                value={inputValue}
                onChange={handleChange}
              />
            </label>
          </div>
          
          {number && <p>You entered: {number}</p>}
          <div className="altHalfDiv">
          <button onClick={startRemote} className="Action-button"><p className='Button-text'>Start Scripts</p></button>
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;
