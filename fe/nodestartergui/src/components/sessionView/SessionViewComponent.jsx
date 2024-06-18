/* eslint-disable no-unused-vars */
/* eslint-disable react-hooks/exhaustive-deps */
import '../../App.css';
import './SessionView.css';
import React, { useState, useEffect, useMemo } from 'react';
import CommandParamsList from '../paramsList/CommandParamsList';
import DataVault from '../../services/dataVault.ts';
import NumberInput from '../numberInput/numberInputComponent';
import CommunicationHandler from './../../services/communicationHandlers/communicationHandler.ts';
import AvailableNodesList from './../runnablenodeList/AvailableNodesListComponent';
import SelectedNodesList from './../runnablenodeList/SelectedNodesListComponent';
import ProgressBar from '../progressBar/ProgressBar.jsx';

function SessionView({ session }) {
  const [lastClickedParamsText, setLastClickedParamsText] = useState("");
  const [paramsList, setParamsList] = useState([]);
  const [availableNodes, setAvailableNodes] = useState([]);
  const [selectedNodes, setSelectedNodes] = useState([]);
  const [numberOfReps, setNumberOfReps] = useState(0);
  const [measuringActive, setMeasuringActive] = useState(false);
  const [processingStatus, setProcessingStatus] = useState({ status: "idle", repetitionNumber: "" });
  const [currentNumber, setCurrentNumber] = useState(0);
  const [maxNumber, setMaxNumber] = useState(0);

  const requestHandler = useMemo(() => {
    return new CommunicationHandler();
  }, []);

  const handleNumberChange = (newNumber) => {
    setNumberOfReps(newNumber);
  };


  

  const measurmenRoutine = () => {
    setMeasuringActive(true);


    const startMeasurement = async () => {
        setMaxNumber(numberOfReps)
        const measurmentParams = {
          selectedScript: session.session_script, 
          selectedParams: lastClickedParamsText, 
          selectedNodes: selectedNodes,
          masterNodeIp: longPressedItem.ip,
          sessionName: session.session_name,
          sessionId: session.session_id,
          repetitionsNumber: numberOfReps
        };
        try {
          await requestHandler.startMeasuringTask(measurmentParams);
        } catch (error) {
          console.error('Error starting data processing:', error);
        }
    };

    startMeasurement();

  };

  const checkProcessingStatus = async () => {
    if (measuringActive) {
      try {
        const status = await requestHandler.fetchDataMeasuringStatus();
        setCurrentNumber(Number(status.repetitionNumber))
        setProcessingStatus(status);
        if(status.status==="idle"){
          setMeasuringActive(false)
          setMaxNumber(0)
          setCurrentNumber(0)
        }
      } catch (error) {
        console.error('Error fetching processing status:', error);
      }
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      checkProcessingStatus();
    }, 2000); 

    return () => clearInterval(interval);
  }, [measuringActive]);

  useEffect(() => {
    const getParamsList = async () => {
      try {
        const dataVault = DataVault.getInstance();
        let data;
        if (dataVault.getDirty("paramsList")) {
          data = await requestHandler.getCmdParams();
        } else {
          data = { 'paramsList': dataVault.getItem("paramsList") };
        }
        setParamsList(data.paramsList);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    }
    const getAvailableNodes=() =>{
      const dataVault = DataVault.getInstance();
      if(!dataVault.getDirty("availableNodes")){
        const data=dataVault.getItem("availableNodes")
        setAvailableNodes(data);
        return
      }
      
      setAvailableNodes([{hostname:"No nodes available",ip:""}])

    }

    getAvailableNodes();


    getParamsList();
  }, [requestHandler]);



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
    <div>
      <div className='wideOutline'>  
        <p id='sessionText'>Active session: {session.session_name}</p>
        <hr id='sessionHr'/>
        <p id='scriptText'>Session script: {session.session_script}</p>   
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
        <div className="selectionOutline"> 
          <CommandParamsList paramsList={paramsList} itemClicked={(value) => { setLastClickedParamsText(value) }} />
        </div>
      </div>
      <div className="selectionOutline">
        <NumberInput value={numberOfReps} label={"Input the number of repetitions:"} onChange={handleNumberChange} />
        <div className="altHalfDiv">
          <div className='measuringButton'>
            <button onClick={measurmenRoutine}><p className='Button-text'>Start measuring</p></button>
          </div>
        </div>
      </div>
      <div className="selectionOutline">
        {measuringActive ? <ProgressBar  currentNumber={currentNumber} maxNumber={maxNumber} />:<></>}
      </div>
    </div>
  );
}

export default SessionView;
