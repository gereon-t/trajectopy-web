import React from "react";
import icon from "../icon.png";
import "./Header.css";

const Header = () => {
    return <header className="header">
        <div className="left-section">
            <img src={icon} className="trajectopy-logo" alt="Icon"></img>
            <div className="trajectopy-text">Trajectopy</div>
        </div>
    </header>
}

export default Header;