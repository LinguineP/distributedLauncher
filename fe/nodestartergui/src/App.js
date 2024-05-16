import './App.css';
import { React, useState } from 'react';
import RunnableNodeList from './runnablenodeList/RunnableNodeListComponent';
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
    let numberOfNodes;
    //if (inputValue.trim() !== '') {
      //numberOfNodes=parseInt(inputValue)
      setNumber(parseInt(numberOfNodes));
    //}


  

    const requestParams={
                          selectedScript:lastClickedItem,
                          selectedNumberOfNodes:numberOfNodes,
                          selectedNodes:selectedNodes ,
                          decentSelected:isToggled
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
  

  const [isToggled, setIsToggled] = useState(false);

  const handleToggle = () => {
    setIsToggled(!isToggled);
  };

  const [number, setNumber] = useState(null);
  const [inputValue, setInputValue] = useState(0);

  const handleChange = (event) => {
    const value = parseInt(event.target.value, 10);
    const minValue = selectedNodes.length;
    if (value >= minValue) {
      setInputValue(value);
    } else {
      setInputValue(minValue);
    }
  };

  /* TODO: add a shutdown nodes button, number of nodes >= selected Nodes , cent/decent choice, maybe check nodes health toast  */

  return (
    <div className="App">
      <header className="App-header">
       <p className='buttonText'>Welcome to distributed app starter</p>
       <button onClick={discovery} className="Action-button"><p className='Button-text'>{discoveryOn ? stopDiscoveryText : startDiscoveryText}</p></button>
       
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
       <div className="availableScripts">
        
          <p>Available Scripts</p>
          <hr></hr>
          <RunnableNodeList items={availableScripts} script={true} onItemClick={itemWasClickedScript} lastClickedItem={lastClickedItem} 
  setLastClickedItem={setLastClickedItem}>

          </RunnableNodeList>      
       </div>
          <div className="selectionOutline">
            <div className="altHalfDiv">
              {

                <div className="selectionOutline">
                  <div className="altHalfDiv">
                    <div className='center-div'>
                      <label>
                          Enter number of nodes:
                       <input
                          type="number"
                          value={inputValue}
                          onChange={handleChange} />
                      </label>
                  </div>
                </div>
                <div className="altHalfDiv">
                  <div className='center-div'>
                      <div className="toggle-switch">
                      <p>{isToggled ? 'Decentralised' : 'Centralised'}</p>
                        <label className="switch">
                          <input type="checkbox" checked={isToggled} onChange={handleToggle} />
                          <span className="slider"></span>
                        </label>
                      </div>
                  </div>
                </div></div>
              }
               
            </div>
            <div className="altHalfDiv">
              <div className="selectionOutline">
                  <div className="altHalfDiv">
                    <div className="center-div">
                      <button onClick={startRemote} className="Action-button"><p className='Button-text'>Start Scripts</p></button>
                    </div>
                  </div>
                  <div className="altHalfDiv">
                    <div className="center-div">
                      <button onClick={stopRemote} className="Action-button"><p className='Button-text'>Shutdown Nodes</p></button>
                    </div>
                  </div>
              </div>
            </div>
        </div>
      </header>
    </div>
  );
}

export default App;
