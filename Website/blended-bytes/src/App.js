// App.js

import React from 'react';
import ChatBox from './Chat/Chatbox';
import './styles.css'; // Import the CSS file
import logo from './logos/header.jpeg'; // Import the SVG logo

function App() {
  const handleSendMessage = (message) => {
    // Handle the message sending logic (you can send it to the backend or update the state in the parent component)
    console.log('Message sent:', message);
  };

  return (
    <div className="app">
      <header>
        <img src={logo} alt="Logo" className="logo" />
      </header>
      <main>
        <ChatBox onSend={handleSendMessage} />
      </main>
    </div>
  );
}

export default App;
