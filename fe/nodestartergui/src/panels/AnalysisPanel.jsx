import '../App.css';
import './panels.css';
import React, { useState,useEffect ,useMemo, useCallback} from 'react';
import DropdownMenu from '../components/dropdownMenu/DropdownMenuComponent';
import DataVault from '../services/dataVault.ts'
import CommunicationHandler from './../services/communicationHandler.ts';
import ExpandableList from '../components/expandableList/expandableList.jsx';
import ImageDisplay from '../components/imageDisplay/ImageDisplay.jsx';



function AnalysisPanel() {

    const requestHandler = useMemo(() => {
        return new CommunicationHandler();
    }, []);

    const [selectedSession, setSelectedSession] = useState(null);
    const [sessionsItems, setSessionsItems] = useState([]);
    const [selectedSessionName, setSelectedSessionName] = useState('');
    const [batchResults, setBatchResults] = useState(null);
    const [sessionResults, setSessionResults] = useState(null);
    const [refreshVar,setRefreshVarstate]=useState(true)
    
    const [showNotification, setShowNotification] = useState(false);
    const [notificationMessage, setNotificationMessage] = useState('');
    const [notificationType, setNotificationType] = useState('');

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

        getSessionsList();

    
    }, [requestHandler]);
    


    const findSession=(sessionName)=>{
        return sessions.find(element => element['session_name'] === sessionName);
    }

    const handleSelectionChange = (value) => {
        setSelectedSessionName(value);
        setSelectedSession(findSession(value));
        
    };


    const doAnalysis=() => {
        const sendCommand=async () => {
            try {

                await requestHandler.doAnalysis(selectedSession);
                setNotificationMessage('Analysis executed successfully!');
                setNotificationType('success');
                setShowNotification(true);
                

            } 
            catch (error) {
                console.error('Error analysing:', error);
                setNotificationMessage('Analysis error,check the server logs or try again!');
                setNotificationType('error');
                setShowNotification(true);
            }
            
            setTimeout(() => {
                setShowNotification(false);
            }, 2000);
        }

        sendCommand()

    }

    const refresh=()=>{
        setRefreshVarstate(false)
        console.log(refreshVar)
    }


    useEffect(() => {
        if(refreshVar===false)
            getResults()
            setRefreshVarstate(true)
        
        
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [refreshVar]);

    useEffect(() => {
        if(selectedSession){
            getResults()
        }
        
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [selectedSession]);


    const exportCsv= () =>{

        const sendCommand=async () => {
            try {

                await requestHandler.exportCsv();
                setNotificationMessage('Csv exported successfully!');
                setNotificationType('success');
                setShowNotification(true);
            } 
            catch (error) {
            console.error('Error exporting csv:', error);
            setNotificationMessage('Error exporting csv,check the server logs try again!');
                setNotificationType('error');
                setShowNotification(true);
            }
            
            setTimeout(() => {
                setShowNotification(false);
            }, 2000);
        }

        sendCommand()
    }


    const getResults = () => {
        const fetchData = async () => {
                try {
                    
                        const batchResultsData = await requestHandler.getBatchResults(selectedSession.session_id);
                        setBatchResults(null)
                        setBatchResults(batchResultsData);

                        
                        const sessionResultsData = await requestHandler.getSessionResults(selectedSession.session_id);
                        setSessionResults(null)
                        setSessionResults(sessionResultsData);
                    
                } catch (error) {
                console.error("Error fetching data:", error);
                }
                };
        fetchData();
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
                                items={sessionsItems} 
                                onSelectionChange={handleSelectionChange}
                                selectedItem={selectedSessionName} 
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
                {showNotification && (
                <div className={`notification ${notificationType}`}>
                    <p>{notificationMessage}</p>
                </div>
                )}
                <div className='selectionOutlineAnalysis'>
                    <div className='sessionBody'>
                        {(batchResults)&&(
                            <ExpandableList  items={batchResults}/> 
                        )}
                    </div>
                    
                </div>
                <div className='line'>
                    <hr />
                </div>
                <div>   
                    {(sessionResults && sessionResults.meanResult!=="Empty" && sessionResults.stdDevResult!=="Empty" && refreshVar) && (
                        <div className="selectionOutline">
                            <div className="altHalfDiv">
                                <ImageDisplay imagePath={sessionResults.meanResult}></ImageDisplay>
                            </div>
                            <div className="altHalfDiv">
                                <ImageDisplay imagePath={sessionResults.stdDevResult}></ImageDisplay>
                            </div>
                        </div>
                    )}
                </div>
                <div className='line'>
                    <hr />
                </div>
                <div className='sessionBody'>

                        <div className="selectionOutline">
                            <div className="altThirdDiv">
                                
                                    <div className='thirdButtonContainer'>
                                    <button onClick={doAnalysis} ><p className='Button-text'>Analyse data</p></button>
                                    </div>
                            </div>
                            <div className="altThirdDiv">
                                <div className='thirdButtonContainer'>
                                <button onClick={exportCsv} ><p className='Button-text'>Export CSV</p></button>
                                </div>
                            </div>
                            <div className="altThirdDiv">
                                    <div className='thirdButtonContainer'>
                                    <button onClick={refresh} ><p className='Button-text'>Refresh results</p></button>
                                    </div>
                            </div>
                        </div>
                        
                        
                        
                    </div>
                </>
            )}            
        </header>

    </div>
    
    );
}


export default AnalysisPanel;
