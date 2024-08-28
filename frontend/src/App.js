'use client'

import React, { useState, useEffect } from "react";
import "./App.css"
import TextField from "@mui/material/TextField";
import { pdfjs } from 'react-pdf';

import MyDocument from "./Document";
import Chatbot from "./Chatbot"

// import pdfjsWorker from "react-pdf/node_modules/pdfjs-dist/webpack";

if (typeof Promise.withResolvers === 'undefined') {
  if (window) {
      // @ts-expect-error This does not exist outside of polyfill which this is doing
      window.Promise.withResolvers = function () {
          let resolve, reject;
          const promise = new Promise((res, rej) => {
              resolve = res;
              reject = rej;
          });
          return { promise, resolve, reject };
      };
  }
}
pdfjs.GlobalWorkerOptions.workerSrc = new URL('pdfjs-dist/legacy/build/pdf.worker.min.mjs', import.meta.url).toString();


function App() {
  const [searchValue, setSearchValue] = useState('');
  const [messages, setMessages] = useState([]);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    // Load the list from local storage on component mount
    const storedInputs = localStorage.getItem('searchHistory');
    if (storedInputs) {
      setHistory(JSON.parse(storedInputs));
    }
  }, []);

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      if (searchValue === e.target.value) {
        return;
      } 
      setSearchValue(e.target.value);   
      
    }
  };

  // Define the callback function
  const addMessage = async (data) => {
    if (messages.length === 0) {
      alert("You need to index paper first");
    }
    if (messages.length > 0) {
      const lastMessage = messages[messages.length - 1];
      if (lastMessage && lastMessage.role === 'user') {
        return;
      }
      if (data.trim()) {
        const currentMessages = [...messages, { role: 'user', content: data }]
        setMessages(currentMessages);
        // Handle backend API call here
        try {
          const response = await fetch(`http://34.209.51.63:8000/chatbot/chat`, {
            method: 'POST',
            headers: {
              "Content-Type": "application/json",
              "accept": "application/json",
            },
            body: JSON.stringify({url: searchValue, prompt: data}),
          });

          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          const res = await response.json();
          setMessages([...currentMessages, { role: 'assistant', content: res.answer }]);
        } catch (error) {
          console.error('There was a problem with the fetch operation:', error);
        }
      }
    }
  };


  return (
    <div className="App">
      <div className="App-header">
        <div className="App-search">
          <TextField
            id="outlined-basic"
            variant="outlined"
            fullWidth
            label="Search"
            onKeyPress={handleKeyPress}
          />
        </div>
      </div>
      <div className="App-content">
        <div className="left-side">
          <div className="history-box">
            <div className="content-header">
              <h3>History</h3>
            </div>
            <div className="history-detail">
              {history && history.map((item, index) => (
                <div key={index} className="history-item" onClick={() => setSearchValue(item.url)}>
                  {item.label}
                </div>
              ))}
            </div>
          </div>
          <div className="chatbot-box">
            <div className="content-header">
              <h3>Chatbot</h3>
            </div>
            <Chatbot messages={messages} addMessage={addMessage}/>
          </div>
        </div>
        <MyDocument url={searchValue} addMessage={addMessage} history={history} setHistory={setHistory} setMessages={setMessages}/>
      </div>
    </div>
  );
}

export default App;

