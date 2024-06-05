import './App.css';
import React,{useState} from 'react';
import BenchmarkPanel from './panels/BenchmarkPanel';
import LauncherPanel from './panels/LauncherPanel';

function App() {
   const [activeComponent, setActiveComponent] = useState('Launcher');

  const renderComponent = () => {
    switch (activeComponent) {
      case 'Launcher':
        return <LauncherPanel/>;
      case 'Benchmark':
        return <BenchmarkPanel/>;
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
              className={`nav-button ${activeComponent === 'Benchmark' ? 'active' : ''} Attention-text`}
              onClick={() => setActiveComponent('Benchmark')}
            >
              Benchmark
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
