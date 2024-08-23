from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from paper_retriever.utils.parsing import parse_pdf2text, parse_references_and_citations, parse_references
from paper_retriever.utils.io import make_working_dir, save_pdf
from paper_retriever.utils.crossref import retrieve_from_crossref


router = APIRouter(
    prefix = '/paper_retriever',
    tags = ['paper_retriever'],
)


@router.get("/")
def read_root():
    return JSONResponse(content={"message": "Welcome to the paper search API"})


@router.post("/index_paper")
def index_paper(file: UploadFile = File(...)):
    try:
        # Set up working directory and save the PDF file
        working_dir = make_working_dir()
        paper_path = save_pdf(working_dir, file) 
        print(f"\nPDF file saved to: {paper_path}")

        # Parse the PDF file's reference section 
        pdf_text = parse_pdf2text(paper_path)
        sample = pdf_text.split('\n')[0]
        print(f"\nPDF text: {sample}")

        # Extract references into structured format
        reference_list, cite_id_type = parse_references_and_citations(pdf_text)
        print(f"\nReference list[0]: {reference_list[0]}")
        parsed_refs = parse_references(reference_list, cite_id_type, working_dir)
        print(f"\nParsed references[0]: {parsed_refs[0]}")

        # Query titles of references by crossref, and filter out results with title that shared high similarity with the query titles
        retrieve_df = retrieve_from_crossref(parsed_refs)
        retrieve_df = retrieve_df[retrieve_df["tf-idf_score"] > 0.7]
        return JSONResponse(status_code=200, content={"message": "The file is a paper.", "data": retrieve_df.to_dict(orient='records')})

    
    except Exception as e:
        raise JSONResponse(status_code=500, content={"message": f"{e}"})
    

# @router.get("/search")
# def search_arxiv(
#     search_query: str = Query(..., description="Search query for arXiv"),
#     max_results: int = Query(10, ge=1, le=100, description="Number of results to retrieve"),
# ):
#     print("Calling search API...")
#     params = {
#         "search_query": search_query,
#         "start": 0,
#         "max_results": max_results,
#     }
    
#     response = requests.get(ARXIV_API_URL, params=params)    
#     if response.status_code != 200:
#         return JSONResponse(status_code=response.status_code, content={"detail": "Error connecting to arXiv API"})   
#     parsed_results = parse_arxiv_response(response.text)
#     # parsed_results = response.text
#     return JSONResponse(content=parsed_results)


# @router.get("/paper")
# def get_paper(
#     paper_doi: str = Query(..., description="DOI of the paper to retrieve"),
# ):
    
#     print("Calling paper API...")
#     print(f"Paper DOI: {paper_doi}")

#     # CrossRef: DOI -> title
#     title = get_title_from_doi(paper_doi)
#     if title is None:        
#         print("Error connecting to arXiv API or paper not found")


#     # arXiv: title -> metadata = {arXiv id, ...} -> PDF file
#     response = requests.get("http://localhost:8000/paper_retriever/search/", params={"search_query": title, "max_results": 1})
#     metadata = response.json()[0]
#     arxiv_id = response.json()[0]['id'].split("/")[-1]
#     print(f"arXiv ID: {arxiv_id}")
#     pdf_url = f"{ARXIV_PDF_URL}{arxiv_id}"
#     response = requests.get(pdf_url)
#     file_path = os.path.join(SHARED_DATA_DIR, f"{paper_doi.replace('/', '_')}.pdf")
#     print(file_path)
#     with open(file_path, "wb") as f:
#         f.write(response.content)

#     # CrossRef: DOI -> references
#     crossref_url = f"{CROSSREF_URL}{paper_doi}"
#     response = requests.get(crossref_url)
#     data = response.json()
    
#     if 'reference' in data['message']:
#         references = data['message']['reference']
#         for ref in references:
#             print(f"{ref.get('key')}\t{ref.get('DOI')}\t{ref.get('title')}")
#     else:
#         print("No references found.")
