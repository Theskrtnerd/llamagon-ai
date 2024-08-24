from fastapi import FastAPI
from paper_retriever.router import router as paper_retriever_router
from ref_retriever.router import router as ref_retriever_router


app = FastAPI()
app.include_router(paper_retriever_router)
app.include_router(ref_retriever_router)