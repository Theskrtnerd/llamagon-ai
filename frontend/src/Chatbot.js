import { React, useState } from 'react'

function Chatbot({messages, addMessage}) {
    const [userInput, setUserInput] = useState('');
  
    const sendMessage = () => {
      if (userInput.trim()) {
        addMessage(userInput);
        setUserInput('');
      }
    };

    const handleInputChange = (e) => {
      setUserInput(e.target.value);
    };
  
    // Handle "Enter" key in input
    const handleKeyPress = (e) => {
      if (e.key === 'Enter') {
        sendMessage();
      }
    };
  return (
      <div className="chatbot-detail">
        <div className="chatbot-content">
          {messages.map((message, index) => (
             message.role !== "system" && <p key={index} className={message.role}>
              {message.content}
            </p>
          ))}
        </div>
        <div className="chatbot-footer">
          <input
            type="text"
            placeholder="Type a message..."
            className="chatbot-input"
            value={userInput}
            onChange={handleInputChange}
            onKeyPress={handleKeyPress}
          />
          <button className="chatbot-button" onClick={sendMessage}>Send</button>
        </div>
      </div>
    )
}

export default Chatbot