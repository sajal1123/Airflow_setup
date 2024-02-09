// MessageBox.js

import React from 'react';
import '../styles.css';
function MessageBox({ messages }) {
  return (
    <div className="message-box">
      {messages.map((message, index) => (
        <div key={index} className={`message ${message.isUser ? 'user-message fade-in' : 'server-message fade-in'}`}>
          {message.text}
        </div>
      ))}
    </div>
  );
}

export default MessageBox;
