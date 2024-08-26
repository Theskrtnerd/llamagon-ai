from pydantic import BaseModel
from typing import List

# Define the input schema
class ChatInput(BaseModel):
    context: str
    question: str

class ExplanationRequest(BaseModel):
    role: str
    content: str

class Item(BaseModel):
    key1: str 
    key2: str
