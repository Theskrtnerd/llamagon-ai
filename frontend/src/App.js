'use client'

import React, { useRef, useState, useEffect, useCallback } from "react";
import "./App.css"
import { pdfjs } from 'react-pdf';
import MyDocument from "./Document";
import 'react-pdf/dist/esm/Page/AnnotationLayer.css'
import 'react-pdf/dist/esm/Page/TextLayer.css'

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
  // const [recommendations, setRecommendations] = useState([]);
  const [content, setContent] = useState('');
  // const [timeoutId, setTimeoutId] = useState(null); // State to store the timeout ID

  // const allRecommendations = ['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry'];

  const handleSearchChange = (event) => {
    const value = event.target.value;
    setSearchValue(value);

    // // Clear the previous timeout if the user continues typing
    // if (timeoutId) {
    //   clearTimeout(timeoutId);
    // }

    // // Set a new timeout
    // const newTimeoutId = setTimeout(() => {
    //   // Filter recommendations based on the search value
    //   if (value.length > 0) {
    //     const filteredRecommendations = allRecommendations.filter(item =>
    //       item.toLowerCase().includes(value.toLowerCase())
    //     );
    //     setRecommendations(filteredRecommendations);
    //   } else {
    //     setRecommendations([]);
    //   }
    // }, 500); // 0.5 seconds delay

    // setTimeoutId(newTimeoutId); // Store the new timeout ID
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      setContent(searchValue);
      // Or if passing via state: navigate('/search', { state: { query: searchValue } });
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <input
          type="search"
          placeholder="Search..."
          className="App-search"
          value={searchValue}
          onChange={handleSearchChange}
          onKeyDown={handleKeyDown}
        />
      </header>
      <div className="content">
        <div className="left-side">
          <div className="reference-box">
            <div className="content-header">
              <h3>References</h3>
            </div>
            <div className="content-detail">
              <p>Test</p>
              <p>Test</p>
            </div>
          </div>
          <div className="chatbot-box">
            <div className="content-header">
              <h3>Chatbot</h3>
            </div>
            <div className="chatbot-detail">
              <div className="chatbot-content">
                <p>Test</p>
              </div>
              <div className="chatbot-footer">
                <input
                  type="text"
                  placeholder="Type a message..."
                  className="chatbot-input"
                />
                <button className="chatbot-button">Send</button>
              </div>
            </div>
          </div>
        </div>
        <div className="right-side">
          <MyDocument />
        </div>
      </div>
    </div>
  );
}

export default App;

