# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from setup import embedding_model
from typing import List


class TextInput(BaseModel):
    text_list: List[str]


app = FastAPI()


@app.post("/compute-embedding/")
async def compute_embedding(input: TextInput):
    try:
        embeddings = embedding_model(input.text_list)
        return JSONResponse(content={"embeddings": embeddings.tolist()})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
