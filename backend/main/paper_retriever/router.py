from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.params import Query
import requests
import os
from paper_retriever.constants import ARXIV_API_URL, ARXIV_PDF_URL, CROSSREF_URL, SHARED_DATA_DIR
from paper_retriever.utils import get_title_from_doi, parse_arxiv_response


router = APIRouter(
    prefix = '/paper_retriever',
    tags = ['paper_retriever'],
)


@router.get("/")
def read_root():
    return JSONResponse(content={"message": "Welcome to the arXiv search API"})


@router.get("/search")
def search_arxiv(
    search_query: str = Query(..., description="Search query for arXiv"),
    max_results: int = Query(10, ge=1, le=100, description="Number of results to retrieve"),
):
    print("Calling search API...")
    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": max_results,
    }
    
    response = requests.get(ARXIV_API_URL, params=params)    
    if response.status_code != 200:
        return JSONResponse(status_code=response.status_code, content={"detail": "Error connecting to arXiv API"})   
    parsed_results = parse_arxiv_response(response.text)
    # parsed_results = response.text
    return JSONResponse(content=parsed_results)


@router.get("/paper")
def get_paper(
    paper_doi: str = Query(..., description="DOI of the paper to retrieve"),
):
    
    print("Calling paper API...")
    print(f"Paper DOI: {paper_doi}")

    # CrossRef: DOI -> title
    title = get_title_from_doi(paper_doi)
    if title is None:        
        print("Error connecting to arXiv API or paper not found")


    # arXiv: title -> metadata = {arXiv id, ...} -> PDF file
    response = requests.get("http://localhost:8000/paper_retriever/search/", params={"search_query": title, "max_results": 1})
    metadata = response.json()[0]
    arxiv_id = response.json()[0]['id'].split("/")[-1]
    print(f"arXiv ID: {arxiv_id}")
    pdf_url = f"{ARXIV_PDF_URL}{arxiv_id}"
    response = requests.get(pdf_url)
    file_path = os.path.join(SHARED_DATA_DIR, f"{paper_doi.replace('/', '_')}.pdf")
    print(file_path)
    with open(file_path, "wb") as f:
        f.write(response.content)

    # CrossRef: DOI -> references
    crossref_url = f"{CROSSREF_URL}{paper_doi}"
    response = requests.get(crossref_url)
    data = response.json()
    
    if 'reference' in data['message']:
        references = data['message']['reference']
        for ref in references:
            print(f"{ref.get('key')}\t{ref.get('DOI')}\t{ref.get('title')}")
    else:
        print("No references found.")
