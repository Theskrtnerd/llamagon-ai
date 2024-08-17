# main.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from setup import embedding_model
from schemas import TextInput


app = FastAPI()


@app.post("/compute-embedding/")
async def compute_embedding(input: TextInput):
    print("Input:")
    for text in input.text_list:
        print(f"{text[:100]}...")
    try:
        embeddings = embedding_model(input.text_list)['dense']
        embeddings_list = [embedding.tolist() for embedding in embeddings]
        print(f"\nComputed {len(embeddings_list)} embeddings with size {embeddings_list[0].__len__()}")
        return JSONResponse(content={"embeddings": embeddings_list})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)