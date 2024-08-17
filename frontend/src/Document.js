import { useState } from 'react';
import { Document, Page } from 'react-pdf';
import pdf from "./paper.pdf";
import "./Document.css"

function MyDocument() {
  const [numPages, setNumPages] = useState();
  const [pageNumber, setPageNumber] = useState(1);

  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
  }

  function goToPrevPage() {
    setPageNumber(prevPageNumber => Math.max(prevPageNumber - 1, 1));
  }

  function goToNextPage() {
    setPageNumber(prevPageNumber => Math.min(prevPageNumber + 1, numPages));
  }

  return (
    <div>
      <div className="page">
      <button onClick={goToPrevPage}>Previous</button>
      <span>Page {pageNumber} of {numPages}</span>
      <button onClick={goToNextPage}>Next</button>
      </div>
      <Document file={pdf} onLoadSuccess={onDocumentLoadSuccess}>
        <Page pageNumber={pageNumber} />
      </Document>
    </div>
  );
}

export default MyDocument;