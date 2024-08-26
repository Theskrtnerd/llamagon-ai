from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from paper_retriever.router import router as paper_retriever_router
from ref_retriever.router import router as ref_retriever_router
from chatbot.router import router as chatbot_router


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Or specify allowed methods like ["GET", "POST"]
    allow_headers=["*"],  # Or specify allowed headers like ["Authorization", "Content-Type"]
)
app.include_router(paper_retriever_router)
app.include_router(ref_retriever_router)
app.include_router(chatbot_router)