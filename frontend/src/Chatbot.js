import { React, useState } from 'react'

function Chatbot() {
    const [messages, setMessages] = useState([
        { role: 'agent', text: 'Hello, how can I help you?' }
      ]);
      const [userInput, setUserInput] = useState('');
    
      // Step 2: Update state on new message
      const sendMessage = () => {
        if (userInput.trim()) {
          setMessages([...messages, { role: 'user', text: userInput }]);
          setUserInput('');
        }
      };
    
      // Handle user typing
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
            {/* Step 3: Display messages */}
            {messages.map((message, index) => (
              <p key={index} className={message.role}>
                {message.text}
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