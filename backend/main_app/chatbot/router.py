from fastapi import APIRouter
from fastapi.responses import JSONResponse
from groq import Groq
from dotenv import load_dotenv
from chatbot.schemas import Item, ChatRequest
import os
import requests
from typing import List
from chatbot.constants import EMBEDDING_URL
import setup
from setup import milvus_client
from pymilvus import Collection
import ast
import json


# Load Milvus collection
paper_collection = Collection("paper_chunks")


# Load the Groq API key from environment variables
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# Define the router
router = APIRouter(
    prefix = '/chatbot',
    tags = ['chatbot'],
)


@router.get("/")
def read_root():
    return JSONResponse(content={"message": "Welcome to the chatbot API"})


@router.post("/chat")
async def chat(payload: ChatRequest):
    url = payload.url
    prompt = payload.prompt
    paper_title = ""
    paper_context = ""

    # Get prompt's embedding
    r = requests.post(EMBEDDING_URL, json={"request_id": 0, "text_list": [prompt]})
    embedding = r.json()["embeddings"]

    # Milvus search for relevant paper chunks
    search_param = {
        "data": embedding,
        "anns_field": "dense_vector",
        "param": {"metric_type": "COSINE", "params": {"nprobe": 10}},
        "limit": 5,
        "expr": f"""url == "{url}" """,
        "output_fields": ["doc"]
    }
    chunk_results = paper_collection.search(**search_param)
    hits = chunk_results[0]
    try:
        for hit in hits:
            doc_content = hit.doc
            paper_context += (doc_content + "\n")
    except:
        return JSONResponse(status_code=404, content={"answer": "Paper does not exist or has not been indexed."})

    # Milvus search for paper title
    title_results = milvus_client.query(
            collection_name="paper_summaries",
            filter=f"""url == "{url}" """,
            output_fields=["paper_title"],
    )
    hits = title_results[0]
    paper_title = hits.get('paper_title', '')

    print(f"Paper title: {paper_title}")
    print(f"Paper context: {paper_context}")

    messages = [
        {
            "role": "system",
            "content": 
                f"""
                You are an AI assistant that explains text or answers user's question from a paper. 
                Given the context from paper {paper_title}, you have to execute user's prompt. There are 2 cases:
                - If user dont input any question, your job is to explain the prompt based on the paper's context.
                - Otherwise, you must answer the question based on the prompt and the paper's context. 
                The paper'scontext is below:
                {paper_context}
                """
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192", 
            messages=messages
        )
        answer = response.choices[0].message.content
        return JSONResponse(status_code=200, content={"answer": answer})    
    except Exception as e:
        raise JSONResponse(status_code=500, content={"error": f"{e}"})



