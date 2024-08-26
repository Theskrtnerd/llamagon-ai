from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ref_retriever.schemas import ReferenceRequest
from ref_retriever.utils.parsing import extract_citation
import setup
from setup import milvus_client
from pymilvus import Collection


# Load Milvus collection
paper_collection = Collection("paper_chunks")
ref_collection = Collection("ref_chunks")


router = APIRouter(
    prefix = '/ref_retriever',
    tags = ['ref_retriever'],
)


@router.get("/")
def read_root():
    return JSONResponse(content={"message": "Welcome to the reference search API"})


@router.post("/search")
def search(input: ReferenceRequest):
    try:
        base_url = input.base_url
        text = input.text
        citations = extract_citation(text)
        print(f"Citations: {citations}")
        results = milvus_client.query(
            collection_name="ref_chunks",
            filter=f"""(base_url == "{base_url}") and (cite_id in {str(citations)})""",
            output_fields=["cite_id", "title", "abstract", "url"],
        )
        return JSONResponse(status_code=200, content={"message": "References extracted.", "data": results})
    except Exception as e:
        raise JSONResponse(status_code=500, content={"message": f"{e}"})