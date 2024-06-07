import '../App.css';
import './panels.css';
import React, { useState,useEffect ,useMemo} from 'react';
import Modal from 'react-modal';
import SessionView from '../components/sessionView/SessionViewComponent';
import DropdownMenu from '../components/dropdownMenu/DropdownMenuComponent';
import AvailableScriptsList from '../components/availableScriptsList/AvailableScriptsListComponent';
import DataVault from '../services/dataVault.ts'
import CommunicationHandler from './../services/communicationHandlers/communicationHandler.ts';
import App from './../App';
import CommandParamsList from './../components/paramsList/CommandParamsList';
import ExpandableItem from '../components/expandableList/expandableList.jsx';
import ExpandableList from '../components/expandableList/expandableList.jsx';



Modal.setAppElement('#root'); 

function AnalysisPanel() {

    const requestHandler = useMemo(() => {
        return new CommunicationHandler();
    }, []);

    const [selectedSession, setSelectedSession] = useState(null);
    const [selectedSessionName, setSelectedSessionName] = useState('');

    const [sessions, setSessions] = useState([{session_id: 1,session_name: "newSessionName", session_script: "lastClickedScriptText"}]);

    const selectSessionPlaceHolder = "--Select a session--";



    const [paramsList, setParamsList] = useState(["2 3 504"]);
    const [selectedParam, setSelectedParam] = useState(null);
    const [selectedParamName, setSelectedParamName] = useState('');


    useEffect(() => {

        const getSessionsList = async () => {
            try {

                const dataVault = DataVault.getInstance();
                let sessionList;
                if(dataVault.getDirty("sessionList")){
                    sessionList= await requestHandler.getSessions();
                }
                else{
                    sessionList=dataVault.getItem("sessionList")
                }

                setSessions(sessionList)
            } 
            catch (error) {
            console.error('Error fetching data:', error);
            }
        }


        const getBatchParams=async () => {
            try {

                const dataVault = DataVault.getInstance();
                let sessionList;
                if(dataVault.getDirty("sessionList")){
                    sessionList= await requestHandler.getSessions();
                }
                else{
                    sessionList=dataVault.getItem("sessionList")
                }

                setSessions(sessionList)
            } 
            catch (error) {
            console.error('Error fetching data:', error);
            }
        }

        //getSessionsList();
        //getBatchParams();

    
    }, [requestHandler]);


    const findSession=(sessionName)=>{
        return sessions.find(element => element['session_name'] === sessionName);
    }

    const handleSelectionSessionChange = (value) => {
        setSelectedSessionName(value)
        setSelectedSession(findSession(value));
    };

    const handleSelectionParamChange = (value) => {
        setSelectedParamName(value)
        setSelectedParam(findSession(value));
    };


    




    const transformSessionsToItems = (sessions) => {
        return sessions.map(session => ({
            id: session.session_id,
            name: (session.session_name+' ('+session.session_script+')')
        }));
    };

    const transformParamsToItems = (paramsList) => {
        return paramsList.map(param=> ({
            id : 1,
            name: param
        }));
    };



return (
    <div className="App">
        <header className='App-header'>
            <div className='panelHeader'>
                <div className='selectionOutlineAnalysis'>
                    <div className='altHalfDivAnalysis'>
                        <p>Select a session:</p>
                    </div>
                    <div className='altHalfDivAnalysis'>
                        <div className='alt75DivAnalysis'>
                            <DropdownMenu 
                            placeholder={selectSessionPlaceHolder} 
                            items={sessions} 
                            onSelectionChange={handleSelectionSessionChange}
                            selectedItem={selectedSession} 
                            transformFunction={transformSessionsToItems}
                            />
                        </div>
                    </div>
                </div>
            </div>
            <div className='line'>
                    <hr />
                </div>
            {(selectedSessionName !== '' ) && (
                <>
                <div className='selectionOutlineAnalysis'>
                    <div className='sessionBody'>
                        <ExpandableList />
                    </div>
                    
                </div>
                <div className='line'>
                    <hr />
                </div>
                <div className='sessionBody'>

                        <div className="selectionOutline">
                            <div className="altHalfDiv">
                                <div className='buttonContainer'>
                                <button ><p className='Button-text'>Analyse data</p></button>
                                </div>
                            </div>
                            <div className="altHalfDiv">
                                <div className='buttonContainer'>
                                <button ><p className='Button-text'>Export CSV</p></button>
                                </div>
                            </div>
                        </div>
                        
                        <p>results</p>
                        
                    </div>
                </>
            )}            
        </header>

    </div>
    
    );
}

export default AnalysisPanel;
