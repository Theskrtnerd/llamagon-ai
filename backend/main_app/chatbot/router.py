from fastapi import APIRouter
from fastapi.responses import JSONResponse
from groq import Groq
from dotenv import load_dotenv
from chatbot.schemas import ExplanationRequest, Item
import os
import requests
from typing import List


# Load the Groq API key from environment variables
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


router = APIRouter(
    prefix = '/chatbot',
    tags = ['chatbot'],
)




@router.post("/items")
async def create_item(item: Item):
    return JSONResponse(status_code=200, content={"item": item.dict()})


@router.post("/ebd")
async def get_ebd(input: str):
    try:
        response = client.embeddings.create(
            model = "llama3-8b-8192", 
            messages = [
                {
                    "role": "system",
                    "content": "You are an AI assistant that generates embeddings."
                },
                {
                    "role": "user",
                    "content": input
                }
            ]
        )
        
        response.raise_for_status()

        ebd = response.choices[0].message.content
        return JSONResponse(status_code=200, content={"ebd": ebd})
    
    except Exception as e:
        raise JSONResponse(status_code=500, content={"message": f"{e}"})


@router.post("/chat")
async def explain_text(requests: List[ExplanationRequest]):
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192", 
            messages=requests
        )
        answer = response.choices[0].message.content
        return JSONResponse(status_code=200, content={"answer": answer})    
    except Exception as e:
        raise JSONResponse(status_code=500, content={"error": f"{e}"})