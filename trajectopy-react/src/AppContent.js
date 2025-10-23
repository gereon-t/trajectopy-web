import React from 'react';
import Header from './components/Header';
import Base from './components/Base';
import Footer from './components/Footer';
import './App.css';

const AppContent = ({ currentSession, initialTrajectories, initialResults, onGoBack }) => (
    <div className="App">
        <Header currentSession={currentSession} onGoBack={onGoBack} />
        <div>
            <div>
                <Base
                    sessionId={currentSession.id}
                    initialTrajectories={initialTrajectories}
                    initialResults={initialResults}
                />
            </div>
        </div>
        <Footer />
    </div>
);

export default AppContent;