import '../../App.css';
import React,{useState,useEffect} from 'react';
import CommandParamsList from '../paramsList/CommandParamsList';
import DataVault from '../../services/dataVault.ts';


function SessionView({ session }) {

    const [lastClickedParamsText, setLastClickedParamsText] = useState("");
    const [paramsList, setParamsList] = useState([]);

    useEffect(() => {
    const dataVault = DataVault.getInstance();
    const params = dataVault.getItem("paramsList");
    if (params) {
      setParamsList(params);
    } else {
      setParamsList(['hello', 'there', 'general', 'kenobi']);
    }
    }, []);

return (
        <div>
            <h3>Active session: {session.session_name} {session.session_script}</h3>    
            <div className="wideOutline">
          <div className="selectionOutline">
            <CommandParamsList paramsList={paramsList}
            itemClicked={(value)=>{setLastClickedParamsText(value) }} />
          </div>
        </div>
        </div>
    );
}

export default SessionView;
