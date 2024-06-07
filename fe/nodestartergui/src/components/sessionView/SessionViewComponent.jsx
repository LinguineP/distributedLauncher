import '../../App.css';
import './SessionView.css'
import React,{useState,useEffect,useMemo} from 'react';
import CommandParamsList from '../paramsList/CommandParamsList';
import DataVault from '../../services/dataVault.ts';
import NumberInput from '../numberInput/numberInputComponent';
import CommunicationHandler from './../../services/communicationHandlers/communicationHandler.ts';


function SessionView({ session }) {

  const [, setLastClickedParamsText] = useState("");
  const [paramsList, setParamsList] = useState([]);
  const [number, setNumber] = useState(0);

  const requestHandler = useMemo(() => {
    return new CommunicationHandler();
    }, []);

  const handleNumberChange = (newNumber) => {
    setNumber(newNumber);
  };

  const startMeasurment =()=>{

  }

    useEffect(() => {
    const getParamsList = async () => {
      try {
        const dataVault = DataVault.getInstance();
        let data
        if(dataVault.getDirty("paramsList")){
          data= await requestHandler.getCmdParams();
        }
        else{
          data={'paramsList':dataVault.getItem("paramsList")}
        }

        
        setParamsList(data.paramsList);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    }

    getParamsList();
    }, [requestHandler]);

return (
        <div>
            <div className='wideOutline'>  
                <p id='sessionText'>Active session: {session.session_name}</p>
                <hr id='sessionHr'/>
                <p id='scriptText'>Session script: {session.session_script}</p>   
            </div>
            
            <div className="wideOutline">
              <div className="selectionOutline"> 
                <CommandParamsList paramsList={paramsList}
                itemClicked={(value)=>{setLastClickedParamsText(value) }} />
              </div>
            </div>
            <div className="selectionOutline">
              <NumberInput value={number} label={"Input the number of repetitions:"}onChange={handleNumberChange} />
              <div className="altHalfDiv">
                <div className='measuringButton'>
                  <button onClick={startMeasurment}><p className='Button-text'>Start measuring</p></button>
                </div>
              </div>
            </div>

        </div>
    );
}

export default SessionView;
