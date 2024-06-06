import '../App.css';
import './panels.css';
import React, { useState,useEffect ,useMemo} from 'react';
import Modal from 'react-modal';
import SessionView from '../components/sessionView/SessionViewComponent';
import DropdownMenu from '../components/dropdownMenu/DropdownMenuComponent';
import AvailableScriptsList from '../components/availableScriptsList/AvailableScriptsListComponent';
import DataVault from '../services/dataVault.ts'
import CommunicationHandler from './../services/communicationHandlers/communicationHandler.ts';



Modal.setAppElement('#root'); 

function BenchmarkPanel() {

   const requestHandler = useMemo(() => {
    return new CommunicationHandler();
  }, []);

  const [selectedSession, setSelectedSession] = useState(null);
  const [selectedSessionName, setSelectedSessionName] = useState('');
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [newSessionName, setNewSessionName] = useState('');
  const [sessions, setSessions] = useState([]);
  const [availableScripts, setAvailableScripts] = useState([]);
  const [lastClickedScriptText, setLastClickedScriptText] = useState("");
  const [lastClickedScript, setLastClickedScript] = useState(null);
  const selectSessionPlaceHolder = "--Select a session--";

  

  useEffect(() => {
    const getSessionsList = async () => {
      try {
      const sessionList=await requestHandler.getSessions()
      setSessions(sessionList)
        } catch (error) {
        console.error('Error fetching data:', error);
      }
    }
    getSessionsList()
  }, [requestHandler]);


  const findSession=(sessionName)=>{
    return sessions.find(element => element['session_name'] === sessionName);
  }

  const handleSelectionChange = (value) => {
    setSelectedSessionName(value)
    setSelectedSession(findSession(value));
  };

  const openModal = () => {
    const dataVault = DataVault.getInstance();
    const scripts = dataVault.getItem("scriptsList");
    if (scripts) {
      setAvailableScripts(scripts);
    } else {
      setAvailableScripts(['hello', 'there', 'general', 'kenobi']);
    }

    setModalIsOpen(true);
  };

  const closeModal = () => {
    setModalIsOpen(false);
  };

  const handleNewSessionNameChange = (e) => {
    setNewSessionName(e.target.value);
  };

  const createNewSession = () => {
    if (newSessionName && lastClickedScriptText) {
      const newSession=requestHandler.postSession({'sessionName': newSessionName, 'sessionScript': lastClickedScriptText});
      setSessions([...sessions, newSession]);
      setSelectedSession(newSession);
      setNewSessionName('');
      closeModal();
    }
  };

   const transformSessionsToItems = (sessions) => {
    return sessions.map(session => ({
      id: session.session_id,
      name: session.session_name
    }));
  };



  const itemWasClickedScript = (item) => {
    setLastClickedScript(item);
    setLastClickedScriptText(item); 

  };

  return (
    <div className="App">
      <header className='App-header'>
        <div className='panelHeader'>
          <div className='selectionOutline'>
            <div className='altHalfDiv'>
              <DropdownMenu 
                placeholder={selectSessionPlaceHolder} 
                items={sessions} 
                onSelectionChange={handleSelectionChange}
                selectedItem={selectedSession} 
                transformFunction={transformSessionsToItems}
              />
            </div>
            <div className='altHalfDiv'>
              <div className='sessionButton'>
                <button onClick={openModal}><p className=''>Make a new session</p></button>
              </div>
            </div>
          </div>
        </div>
        <div className='sessionBody'>
          <div className='selectionOutline'>
            {selectedSessionName !== '' && (
              <SessionView session={selectedSession} />
            )}
          </div>
        </div>
        <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        contentLabel="Create New Session"
        className="Modal"
        overlayClassName="Overlay"
        >
            <div className='modal-container'>
              <h1 id='createSessionTitle'>Create a new session</h1>
              <div className='selectionOutline'>
                <div className='altHalfDiv'>
                  <div className='borderedOutline'>
                    <h4 id='selectScripth4'> Select the session script</h4>
                    <hr/>
                    <div className='createSessionScripts'>
                      <AvailableScriptsList 
                        items={availableScripts}  
                        onItemClick={itemWasClickedScript} 
                        lastClickedScript={lastClickedScript} 
                        setLastClickedScript={setLastClickedScript}
                      />
                    </div>
                  </div>
                </div>
                <div className='altHalfDiv'>
                  <div className='borderedOutline'>
                    <h4>
                      <input className='createSessionInput' 
                        type="text" 
                        value={newSessionName} 
                        onChange={handleNewSessionNameChange} 
                        placeholder="Enter session name" 
                      />
                    </h4>
                    <hr />
                    <div className='paddingClass'><p></p></div>
                    <div className='selectionOutline'>
                      <div className='altHalfDiv'>
                        <div className='buttonContainer'>
                          <button className='add-button' onClick={createNewSession}>Create</button>
                        </div>
                      </div>
                      <div className='altHalfDiv'>
                        <div className='buttonContainer'>
                          <button className='cancel-button' onClick={closeModal}>Cancel</button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
        </Modal>
      </header>
    </div>
  );
}

export default BenchmarkPanel;
