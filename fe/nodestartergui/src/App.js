import './App.css';
import React,{useState} from 'react';
import LauncherPanel from './panels/LauncherPanel';
import AnalysisPanel from './panels/AnalysisPanel';
import MeasurementPanel from './panels/MeasurementPanel';

function App() {
   const [activeComponent, setActiveComponent] = useState('Launcher');

  const renderComponent = () => {
    switch (activeComponent) {
      case 'Launcher':
        return <LauncherPanel/>;
      case 'Measurement':
        return <MeasurementPanel/>;
      case 'Analysis':
        return <AnalysisPanel/>
      default:
        return <LauncherPanel/>;
    }
  };

  return (
     <div className="app">
      <nav className="navbar">
        <ul className="nav-list">
          <li className="nav-item">
            <button
              className={`nav-button ${activeComponent === 'Launcher' ? 'active' : ''} Attention-text`}
              onClick={() => setActiveComponent('Launcher')}
            >
              Launcher
            </button>
          </li>
          <li className="nav-item">
            <button
              className={`nav-button ${activeComponent === 'Measurement' ? 'active' : ''} Attention-text`}
              onClick={() => setActiveComponent('Measurement')}
            >
              Measurement
            </button>
          </li>
          <li className="nav-item">
            <button
              className={`nav-button ${activeComponent === 'Analysis' ? 'active' : ''} Attention-text`}
              onClick={() => setActiveComponent('Analysis')}
            >
              Analysis
            </button>
          </li>
        </ul>
      </nav>
      <div className="content">
        {renderComponent()}
      </div>
    </div>
  );
}


export default App;
