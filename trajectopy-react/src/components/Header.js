import React from "react";
import icon from "../icon.png";
import "./Header.css";

const Header = ({ currentSession, onGoBack }) => {
    const sessionName = currentSession.name || `ID: ${currentSession.id}`;
    return <header className="header">
        <div className="left-section">
            <img src={icon} className="trajectopy-logo" alt="Icon"></img>
            <div className="trajectopy-text">Trajectopy</div>
        </div>
        <div className="header-right">
            <div className="session-info">
                <span className="session-label">Current Session:</span>
                <span className="session-name" title={currentSession.id}>
                    {sessionName}
                </span>
            </div>
            <button className="button-secondary" onClick={onGoBack}>
                Change Session
            </button>
        </div>
    </header>
}

export default Header;