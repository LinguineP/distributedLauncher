import '../../App.css';
import React from 'react';


function SessionView({ sessionName }) {


return (
        <div>
            <h3>Active session: {sessionName}</h3>    
        </div>
    );
}

export default SessionView;
