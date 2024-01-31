import Header from './components/Header';
import './App.css';
import Base from './components/Base';
import React, { useState, useEffect } from 'react';
import { createSession } from './api';


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
      <footer className='footer'>
        <div className='footer-items'>
          <a href='https://github.com/gereon-t/trajectopy-web'>gereon-t/trajectopy-web</a>
          <div className='footer-divider'></div>
          <a href='https://github.com/gereon-t/trajectopy'>Desktop App</a>
        </div>
      </footer>
    </div >
  );
}

export default App;
