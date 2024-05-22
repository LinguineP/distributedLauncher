import './App.css';
import { React, useState } from 'react';
import RunnableNodeList from './runnablenodeList/RunnableNodeListComponent';
import CommandParamsList from './paramsList/CommandParamsList.jsx';
import CommunicationHandler from './communicationHandlers/communicationHandler.ts'


function App() {
  
  const requestHandler=new CommunicationHandler();

  const [discoveryOn, setDiscoveryOn] = useState(false);
  const startDiscoveryText="Start discovery";
  const stopDiscoveryText="Stop discovery";
  

  const [availableNodes,setAvailableNodes]=useState([]);
  const [selectedNodes,setSelectedNodes]=useState([]);


  const [availableScripts,setAvailableScripts]=useState([])
  

  const discovery=async()=>{
    setDiscoveryOn(!discoveryOn)
    if(!discoveryOn){
      console.log(false)
      requestHandler.startScan();
      return
    }
    const response=await requestHandler.stopScan();
    console.log(response)


    setAvailableNodes(response.availableNodes);
    setAvailableScripts(response.availableScripts);
  
    console.log(true)
  };
  
  const startRemote=async()=>{
 

  

    const requestParams={
                          selectedScript:lastClickedItem,
                          selectedParams:' ', //TODO
                          selectedNodes:selectedNodes ,
                          
                        }
    requestHandler.startNodes(requestParams);
                
  };


  const stopRemote=async()=>{

    const requestParams={
                          selectedNodes:selectedNodes 
                        }
    requestHandler.stopNodes(requestParams);
                
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
  


  

  const [lastClickedItem, setLastClickedItem] = useState(null);


  
  const itemWasClickedScript = (item) => {
    setLastClickedItem(item)
  };
  


  

 

  /* TODO: add a shutdown nodes button, number of nodes >= selected Nodes , cent/decent choice, maybe check nodes health toast  */

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
              <RunnableNodeList items={availableNodes}  script={false} onItemClick={itemWasClickedAvailable}>
              </RunnableNodeList>
            </div>
            <div className="halfDiv">
              <p>Selected Nodes</p>
              <hr></hr>
              <RunnableNodeList items={selectedNodes} script={false} onItemClick={itemWasClickedSelected}>
              </RunnableNodeList>
            </div>
        </div>

        <div className="wideOutline">
          
            <p>Available Scripts</p>
            <hr></hr>
            <RunnableNodeList items={availableScripts} script={true} onItemClick={itemWasClickedScript} lastClickedItem={lastClickedItem} 
                          setLastClickedItem={setLastClickedItem}>
            </RunnableNodeList>      
        </div>
        <div className="wideOutline">
              <div className="selectionOutline">
              
                  
                  <CommandParamsList></CommandParamsList>
              
                
              </div>
          </div>


          <div className="selectionOutline">
              <div className="altHalfDiv">
                    <div className='buttonContainer'>  
                        <button onClick={startRemote} ><p className='Button-text'>Start Scripts</p></button>
                    </div>
                    
              </div>
              <div className="altHalfDiv">
                  <div className='buttonContainer'>
                        <button onClick={stopRemote} ><p className='Button-text'>Shutdown Nodes</p></button>
                  </div>
              </div>
          </div>
        </header>
    </div>
  );
}


export default App;
