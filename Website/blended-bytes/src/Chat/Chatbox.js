// ChatBox.js

import React, { useState } from 'react';
import MessageBox from './MessageBox';
import UserInput from './UserInput';
import * as constants from '../config.js';
import '../styles.css';

function ChatBox() {
  const [messages, setMessages] = useState([]);
  const tempState = { message: "Waiting for Response...", isUser: false};
  // const [tempState, setTempState] = useState({});

  const api_send_message = constants.chat_send_message;
  console.log("api endpoint = ", api_send_message);

  const handleSendMessage = async (messageText) => {
    setMessages((prevMessages) => [{ text: messageText, isUser: true }, ...prevMessages]);
    setMessages((prevMessages) => [tempState, ...prevMessages]);


    try {
      console.log("messageText = ", typeof(messageText), messageText);
      // Make an API call to the backend with the user's message
      const response = await fetch(api_send_message, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: messageText }),
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      // Parse the response JSON and update the state with the new message

      const responseData = await response.json();
      setMessages((prevMessages) => {
        const updatedMessages = [...prevMessages];
        if (updatedMessages.length > 0) {
          updatedMessages[0] = { text: responseData.summary, isUser: false };
        }
        return updatedMessages;
      });
      
    } catch (error) {
      console.error('Error sending message:', error.message);
    }
  };

  return (
    <div className="chat-box">
      <MessageBox messages={messages} />
      <UserInput onSend={handleSendMessage} />
    </div>
  );
}

export default ChatBox;
