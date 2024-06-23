import '../App.css';
import './panels.css';
import React, { useState, useEffect, useMemo, useCallback } from 'react';
import Modal from 'react-modal';
import SessionView from '../components/sessionView/SessionViewComponent.jsx';
import DropdownMenu from '../components/dropdownMenu/DropdownMenuComponent.jsx';
import AvailableScriptsList from '../components/availableScriptsList/AvailableScriptsListComponent.jsx';
import DataVault from '../services/dataVault.ts'
import CommunicationHandler from '../services/communicationHandler.ts';

Modal.setAppElement('#root'); 

function MeasurmentPanel() {
  const requestHandler = useMemo(() => new CommunicationHandler(), []);

  const [selectedSession, setSelectedSession] = useState(null);
  const [selectedSessionName, setSelectedSessionName] = useState('');
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [newSessionName, setNewSessionName] = useState('');
  const [sessions, setSessions] = useState([]);
  const [sessionsItems, setSessionsItems] = useState([]);
  const [availableScripts, setAvailableScripts] = useState([]);
  const [lastClickedScriptText, setLastClickedScriptText] = useState("");
  const [lastClickedScript, setLastClickedScript] = useState(null);
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
    const getSessionsList = async () => {
      try {
        const dataVault = DataVault.getInstance();
        let sessionList;
        if (dataVault.getDirty("sessionList")) {
          sessionList = await requestHandler.getSessions();
          dataVault.setItem("sessionList", sessionList);
        } else {
          sessionList = dataVault.getItem("sessionList");
        }
        setSessions(sessionList);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    getSessionsList();
  }, [requestHandler]);

  useEffect(() => {
    if (sessions.length) {
      transformSessionsToItems();
    }
  }, [sessions, transformSessionsToItems]);

  const findSession = (sessionName) => {
    return sessions.find(element => element['session_name'] === sessionName);
  };

  const handleSelectionChange = (value) => {
    setSelectedSessionName(value);
    setSelectedSession(findSession(value));
  };

  const openModal = () => {
    const dataVault = DataVault.getInstance();
    const scripts = dataVault.getItem("availableScripts");
    if (scripts) {
      setAvailableScripts(scripts);
    }
    setModalIsOpen(true);
  };


  const handleNewSessionNameChange = (e) => {
    setNewSessionName(e.target.value);
  };

  const createNewSession = () => {
    const newSession = async () => {
      if (newSessionName && lastClickedScriptText) {
        const newSessionResponse = await requestHandler.postSession({ 'sessionName': newSessionName, 'sessionScript': lastClickedScriptText });
        const newSessionItem = newSessionResponse[0];
        const dataVault = DataVault.getInstance();
        let sessionList = dataVault.getItem("sessionList") || [];
        sessionList = [...sessionList, newSessionItem];
        dataVault.setItem("sessionList", sessionList);
        setSessions(sessionList);
        setSelectedSession(newSessionItem);
        setSelectedSessionName(newSessionItem.session_name);
        closeModal();
        // Reset selected script and input field
        setLastClickedScript(null);
        setLastClickedScriptText("");
        setNewSessionName("");
      }
    };
    newSession();
  };

  const closeModal = () => {
  // Reset selected script and input field
    setLastClickedScript(null);
    setLastClickedScriptText("");
    setNewSessionName("");
    setModalIsOpen(false);
  };

  const itemWasClickedScript = (item) => {
    setLastClickedScript(item);
    setLastClickedScriptText(item);
  };

  return (
    <div className="App">
      <header className='App-header'>
        <div className='panelHeader'>
          <div className='selectionOutlineNewSession'>
            <div className='altHalfDiv'>
              <DropdownMenu 
                placeholder={selectSessionPlaceHolder} 
                items={sessionsItems} 
                onSelectionChange={handleSelectionChange}
                selectedItem={selectedSessionName} 
              />
            </div>
            <div className='altHalfDiv'>
              <div className='sessionButton'>
                <button onClick={openModal}><p className=''>Make a new session</p></button>
              </div>
            </div>
          </div>
        </div>
        <div className='line'>
          <hr />
        </div>
        {selectedSessionName !== '' && (
          <div className='sessionBody'>
            <div className='selectionOutline'>
              <SessionView session={selectedSession} />
            </div>
          </div>
        )}
      </header>
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
    </div>
  );
}

export default MeasurmentPanel;
