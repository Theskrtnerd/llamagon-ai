# LlamagonAI - AI Research Paper Reading Assistant

## Overview

LlamagonAI is an AI-powered research paper reading assistant designed to streamline the process of reading, understanding, and retrieving information from academic papers. Leveraging advanced techniques in Retrieval-Augmented Generation (RAG) and the Arxiv API, LlamagonAI makes it easier for researchers to focus on the important aspects of a paper without the hassle of going through every detail.

## Key Features

1. **Interactive Paper Reading**
LlamagonAI allows researchers to actively interact with papers by selecting specific sections of text and asking the system to explain or summarize the content.

2. **Smart Citation Retrieval**
With one-click access, LlamagonAI retrieves reference papers directly, saving time and effort in finding related work.

## System Design
LlamagonAI consists of three core modules, all hosted within a Docker container served using FastAPI:

1. **Paper Indexing Module**
- PDF to Text Conversion: Uses pypdf to convert PDF files into text.
- Document Chunking: Text is split into manageable chunks for processing.
- Metadata Extraction: Uses regex to identify and extract metadata from the references section, parsing it with AnyStyle.io.
- URL Construction: Constructs URLs for reference papers using arXiv IDs or Crossref API when necessary.

2. **Reference Retriever Module**
- Citation Parsing: Users can select text with citation symbols, and the system maps these citations to URLs for easy access.

3. **Chatbot Module**
- Contextual Q&A: Users can ask questions or request explanations of selected text. The system retrieves relevant document chunks and uses Groq API for answering.

Vector Embedding Service
Model: Uses BAAI/bge-m3 hosted on Hugging Face for embedding text and metadata.
Database: Integrates with Milvus vector database for efficient hybrid search (vector search + metadata filter).
Demo
Explore how LlamagonAI enhances your research workflow in the Demo section.

## Getting Started
Prerequisites:
- Docker
- Python 3.8+
- FastAPI
- Hugging Face API

## Installation
- Clone the repository: ```git clone [git@github.com:Theskrtnerd/llamagon-ai.git](https://github.com/Theskrtnerd/llamagon-ai.git)```
- Navigate to the project directory: ```cd llamagonai```
- Frontend:
  ```
  cd frontend
  npm install
  npm start
  ```
- Backend:
- Install and run Milvus:
  ```
  cd backend/milvus
  docker compose up --build
  ```
- Build image for embedding service:
  ```
  cd backend/embedding
  docker build -t ebd .
  docker run --gpus all -p 8003:8003 ebd
  ```
- Build image for main service:
  ```
  cd backend/main_app
  docker build -t main .
  docker run -p 8000:8000 main
  ```
