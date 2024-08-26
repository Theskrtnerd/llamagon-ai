from pydantic import BaseModel
from typing import List

# Define the input schema
class ChatInput(BaseModel):
    context: str
    question: str

class ChatRequest(BaseModel):
    url: str
    prompt: str

class Item(BaseModel):
    key1: str 
    key2: str

class ChatWithPaperRequest(BaseModel):
    url: str
    text: str
