from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
from pydantic import BaseModel

app = FastAPI()

# Load the GROQ API key from environment variables

# Define the input schema
class ChatInput(BaseModel):
    context: str
    question: str

@app.post("/chat-with-context/")
async def chat_with_context(input: ChatInput):
    try:
        context = input.context
        question = input.question

        # Prepare the prompt with context and question
        prompt = f"Context: {context}\n\nQuestion: {question}"

        response = client.chat.completions.create(model="llama3-8b-8192", 
        messages=[
            {"role": "system", "content": "You are an assistant."},
            {"role": "user", "content": prompt}
        ])

        answer = response.choices[0].message.content

        print(f"Question: {question}")
        print(f"Answer: {answer}")

        return JSONResponse(content={"question": question, "answer": answer})
    except Exception as e:
        print(str(e))
        return JSONResponse(content={"error": str(e)}, status_code=500)
