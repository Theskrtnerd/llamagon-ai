<script setup lang="ts">
import { getDocument, GlobalWorkerOptions } from 'pdfjs-dist';

// Set workerSrc to the appropriate path
GlobalWorkerOptions.workerSrc = '/pdf.worker.mjs';

const url = "https://pdfobject.com/pdf/sample.pdf";

const renderPdf = async () => {
  try {
    const loadingTask = getDocument(url);
    const pdf = await loadingTask.promise;
    console.log("PDF loaded");

    const pageNumber = 1;
    const page = await pdf.getPage(pageNumber);
    console.log("Page loaded");

    const scale = 1;
    const viewport = page.getViewport({ scale: scale });

    const canvas = document.getElementById("the-canvas") as HTMLCanvasElement;
    const context = canvas.getContext("2d");
    canvas.height = viewport.height;
    canvas.width = viewport.width;

    const renderContext = {
      canvasContext: context,
      viewport: viewport,
    };
    const renderTask = page.render(renderContext);
    await renderTask.promise;
    console.log("Page rendered");
  } catch (err) {
    console.log(err);
  }
};

renderPdf();
</script>

<template>
  <h2>This is an example of how to display a PDF using PDF.js in a Vue component.</h2>
  <canvas id="the-canvas"></canvas>
</template>
