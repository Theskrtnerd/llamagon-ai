from pydantic import BaseModel
from typing import List

class ChatInput(BaseModel):
    question: str
    embeddings_list: List[List[float]]  # Assuming embeddings are a list of lists (2D list)
