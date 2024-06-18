import '../App.css';
import './panels.css';
import React, { useState,useEffect ,useMemo, useCallback} from 'react';
import DropdownMenu from '../components/dropdownMenu/DropdownMenuComponent';
import DataVault from '../services/dataVault.ts'
import CommunicationHandler from './../services/communicationHandlers/communicationHandler.ts';
import ExpandableList from '../components/expandableList/expandableList.jsx';



function AnalysisPanel() {

    const requestHandler = useMemo(() => {
        return new CommunicationHandler();
    }, []);

    const [selectedSession, setSelectedSession] = useState(null);
    const [sessionsItems, setSessionsItems] = useState([]);
    const [selectedSessionName, setSelectedSessionName] = useState('');

    const [sessions, setSessions] = useState([]);

    const selectSessionPlaceHolder = "--Select a session--";


    const transformSessionsToItems = useCallback(() => {
        const items = sessions.map(item => {
        if (item && item.session_id && item.session_name) {  
            return {
            id: item.session_id,
            name: item.session_name
            };
        }
        console.error('Invalid session item:', item);  
        return null;
        }).filter(item => item !== null);  
        
        setSessionsItems(items);
    }, [sessions]);

    useEffect(() => {
        if (sessions.length) {
            transformSessionsToItems();
        }
    }, [sessions, transformSessionsToItems]);

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

        getSessionsList();
        getBatchParams();

    
    }, [requestHandler]);


    const findSession=(sessionName)=>{
        return sessions.find(element => element['session_name'] === sessionName);
    }

    const handleSelectionSessionChange = (value) => {
        setSelectedSessionName(value)
        setSelectedSession(findSession(value));
    };

    const doAnalysis=() => {
        const sendCommand=async () => {
            try {

                await requestHandler.doAnalysis(selectedSession);

            } 
            catch (error) {
            console.error('Error exporting csv:', error);
            }
        }

        sendCommand()

    }


    const exportCsv= () =>{

        const sendCommand=async () => {
            try {

                await requestHandler.exportCsv();

            } 
            catch (error) {
            console.error('Error exporting csv:', error);
            }
        }

        sendCommand()
    }




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
                            items={sessionsItems} 
                            onSelectionChange={handleSelectionSessionChange}
                            selectedItem={selectedSession} 
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
                                <button onClick={doAnalysis} ><p className='Button-text'>Analyse data</p></button>
                                </div>
                            </div>
                            <div className="altHalfDiv">
                                <div className='buttonContainer'>
                                <button onClick={exportCsv} ><p className='Button-text'>Export CSV</p></button>
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
