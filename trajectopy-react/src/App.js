import Header from './components/Header';
import './App.css';
import Base from './components/Base';
import React, { useState, useEffect } from 'react';
import { createSession } from './api';
import Footer from './components/Footer';


const App = () => {

  const [sessionId, setCurrentSessionId] = useState(null);

  useEffect(() => {
    async function handleSession() {
      console.log('Creating new session...');
      const responseData = await createSession();

      if (responseData === undefined) {
        console.error('Failed to create new session.');
        return;
      }

      setCurrentSessionId(responseData.id);
      console.log('New session created:', responseData.id);
    };
    handleSession();
  }, []);


  return (
    <div className="App">
      <Header />
      <div className="container">
        <div>
          <Base sessionId={sessionId} />
        </div>
      </div>
      <Footer />
    </div >
  );
}

export default App;
