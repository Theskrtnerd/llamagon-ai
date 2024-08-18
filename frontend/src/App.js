'use client'

import React, { useRef, useState, useEffect, useCallback } from "react";
import "./App.css"
import TextField from "@mui/material/TextField";
import { pdfjs } from 'react-pdf';
import MyDocument from "./Document";
import Chatbot from "./Chatbot"
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

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      setSearchValue(e.target.value);
      console.log(e.target.value);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="App-search">
          <TextField
            id="outlined-basic"
            variant="outlined"
            fullWidth
            label="Search"

            onKeyPress={handleKeyPress}
          />
        </div>
      </header>
      <div className="content">
        <div className="left-side">
          <div className="reference-box">
            <div className="content-header">
              <h3>References</h3>
            </div>
            <div className="reference-detail">
              <p>Test</p>
              <p>Test</p>
              <p>Test</p>
              <p>Test</p>
              <p>Test</p>
              <p>Test</p>
              <p>Test</p>
              <p>Test</p>
              <p>Test</p>
              <p>Test</p>
              <p>Test</p>
              <p>Test</p>
              <p>Test</p>
              <p>Test</p>
            </div>
          </div>
          <div className="chatbot-box">
            <div className="content-header">
              <h3>Chatbot</h3>
            </div>
            <Chatbot />
          </div>
        </div>
        <div className="right-side"
          onContextMenu={(e) => {
            e.preventDefault();
            console.log("Content: ", window.getSelection().toString());
          }}
          >
          <MyDocument />
        </div>
      </div>
    </div>
  );
}

export default App;

