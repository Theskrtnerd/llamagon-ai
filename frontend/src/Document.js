import { useState, useEffect } from 'react';
import { Document, Page } from 'react-pdf';
import "./Document.css"
import 'react-pdf/dist/esm/Page/AnnotationLayer.css'
import 'react-pdf/dist/esm/Page/TextLayer.css'

const refs = ["Test1", "Test2", "Test3"];
const listRefs = refs.map((ref) => 
  <li>
    {ref}
  </li>
);

function MyDocument( {url, addMessage, history, setHistory, setMessages} ) {
  const [numPages, setNumPages] = useState();
  const [pageNumber, setPageNumber] = useState(1);
  const [clicked, setClicked] = useState(false);
  const [selectedContent, setSelectedContent] = useState("");
  const [points, setPoints] = useState({
    x: 0,
    y: 0,
  });

  const sendMessage = () => {
    if (selectedContent.trim()) {
      addMessage(selectedContent);
    }
  };
  useEffect(() => {
    const handleClick = () => setClicked(false);
    window.addEventListener("click", handleClick);
    return () => {
      window.removeEventListener("click", handleClick);
    };
  }, []);
  async function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
    try {
      const response = await fetch(`http://34.209.51.63:8000/paper_retriever/context`, {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
          "accept": "application/json",
        },
        body: JSON.stringify({url: url}),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const res = await response.json();
      alert("Loaded context");
      setMessages([{ role: 'system', content: `You are an useful assistant. You need to explain or answer user query based on the context: ${res.data}` }]);
    } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
    }
    if (history.includes(url)) {
        return;
    }
    setHistory([...history, url]);
    localStorage.setItem('searchHistory', JSON.stringify([...history, url]));
  }

  function goToPrevPage() {
    setPageNumber(prevPageNumber => Math.max(prevPageNumber - 1, 1));
  }

  function goToNextPage() {
    setPageNumber(prevPageNumber => Math.min(prevPageNumber + 1, numPages));
  }
  const display = (x, y) => ({
    left: x,
    top: y,
    position: "fixed",
    zIndex: 99,
  });

  return (
    <div className="right-side"
      onContextMenu={(e) => {
        e.preventDefault();
        setClicked(true);
        setPoints({
          x: e.pageX,
          y: e.pageY,
        });
        setSelectedContent(window.getSelection().toString());
      }}
    >
      {clicked && (
        <div className='submenu' style={display(points.x, points.y)}>
          <ul>
            <li onClick={sendMessage}>Explain</li>
            <li>
              References
              <ul className='submenu-items'>
                {listRefs}
              </ul>
            </li>
          </ul>
        </div>
      )}
      <div className="page">
        <button onClick={goToPrevPage}>Previous</button>
        <span>Page {pageNumber} of {numPages}</span>
        <button onClick={goToNextPage}>Next</button>
      </div>
      <div className="document-content">
        <Document file={url} onLoadSuccess={onDocumentLoadSuccess}>
          {Array.from(
            new Array(numPages),
            (el, index) => (
              <Page key={`page_${index + 1}`} pageNumber={index + 1} />
            )
          )}
        </Document>
      </div>
    </div>
  );
}

export default MyDocument;