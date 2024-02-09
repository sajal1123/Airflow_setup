// UserInput.js

import React, { useState } from 'react';

function UserInput({ onSend }) {
  const [message, setMessage] = useState('');

  const sendMessage = () => {
    if (message.trim() !== '') {
      onSend(message);
      setMessage('');
    }
  };

  return (
    <div className="user-input">
      <input
        type="text"
        placeholder="Type your message..."
        className="message-input"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default UserInput;
