from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.params import Body
from ref_retriever.schemas import TextInput
from ref_retriever.utils.parsing import extract_citation


router = APIRouter(
    prefix = '/ref_retriever',
    tags = ['ref_retriever'],
)


@router.get("/")
def read_root():
    return JSONResponse(content={"message": "Welcome to the reference search API"})


@router.post("/search")
def search(input: TextInput):
    try:
        text = input.text
        print(f"Input: {text[:100]}...")
        citations = extract_citation(text)
        return JSONResponse(status_code=200, content={"message": "References extracted.", "data": citations})
    except Exception as e:
        raise JSONResponse(status_code=500, content={"message": f"{e}"})