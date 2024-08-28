from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from paper_retriever.utils.parsing import parse_pdf2text, parse_references_and_citations, parse_references
from paper_retriever.utils.io import make_working_dir, generate_unique_id, download_pdf, save_pdf
from paper_retriever.utils.crossref import retrieve_from_crossref
from paper_retriever.utils.arxiv import get_arxiv_title_by_url
from paper_retriever.utils.summary import summarize_text
from paper_retriever.utils.preprocess import split_pdf
import paper_retriever.utils.indexing
from paper_retriever.utils.indexing import index_paper_chunks, index_references, index_summary
import setup
from setup import milvus_client
from paper_retriever.schemas import URLInput
from pymilvus import Collection


# Load Milvus collection
paper_collection = Collection("paper_chunks")
ref_collection = Collection("ref_chunks")
summary_collection = Collection("paper_summaries")


router = APIRouter(
    prefix = '/paper_retriever',
    tags = ['paper_retriever'],
)


@router.get("/")
def read_root():
    return JSONResponse(content={"message": "Welcome to the paper search API"})


@router.post("/index_paper")
async def index_paper(input: URLInput):
    try:    
        url = input.url
        title = get_arxiv_title_by_url(url)

        # Check existence of the URL in the Milvus DB before indexing to paper_chunks and ref_chunks collection
        query_result = milvus_client.query(
            collection_name="paper_chunks", 
            filter=f"url == '{url}'",        
        )
        if query_result:
            print(f"\nPaper has already been indexed to paper_chunks.")
            return JSONResponse(status_code=200, content={"message": "Paper has already been indexed", "title": title})
        
        # Download PDF file
        raw_file = download_pdf(url)
        if raw_file is None:
            return JSONResponse(status_code=400, content={"message": "Request failed.", "error": "PDF file cannot be downloaded."})
        file_name = generate_unique_id(url) + ".pdf"
        working_dir = make_working_dir()
        paper_path = save_pdf(working_dir, file_name, raw_file)
        print(f"\nPDF file saved to: {paper_path}")

        # Parse the PDF file's reference section 
        pdf_text = parse_pdf2text(paper_path)
        sample = pdf_text.split('\n')[0]
        print(f"\nPDF text: {sample}")

        # Index the paper into paper_chunks collection
        await index_paper_chunks(url, paper_path)
        await index_summary(url, "default summary")

        # Extract references into structured format
        reference_list, cite_id_type = parse_references_and_citations(pdf_text)
        parsed_refs = parse_references(reference_list, cite_id_type, working_dir)

        # Query titles of references by crossref, and filter out results with title that shared high similarity with the query titles
        retrieve_df = retrieve_from_crossref(parsed_refs)
        retrieve_df = retrieve_df[retrieve_df["tf-idf_score"] > 0.7]

        # Index into ref_chunks collection      
        await index_references(url, retrieve_df)

        return JSONResponse(status_code=200, content={"message": "Paper is indexed successfully.", "title": title, "data": retrieve_df.to_dict(orient='records')})
    
    except Exception as e:
        raise JSONResponse(status_code=500, content={"message": f"{e}"})
