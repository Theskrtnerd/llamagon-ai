from fastapi import APIRouter
from fastapi.responses import JSONResponse
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
from pydantic import BaseModel


# Load the OpenAI API key from environment variables

# Define the input schema
class ChatInput(BaseModel):
    context: str
    question: str


router = APIRouter(
    prefix = '/chatbot',
    tags = ['chatbot'],
)


@router.post("/chat-with-context/")
async def chat_with_context(input: ChatInput):
    try:
        context = input.context
        question = input.question

        # Prepare the prompt with context and question
        prompt = f"Context: {context}\n\nQuestion: {question}"

        response = client.chat.completions.create(model="gpt-4o-mini", 
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
