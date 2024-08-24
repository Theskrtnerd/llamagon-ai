from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_milvus.utils.sparse import BM25SparseEmbedding
from typing import List, Dict
import asyncio
import httpx
import pymilvus
import nltk
nltk.download('punkt_tab')
from pymilvus import MilvusClient, Collection, utility, connections


# Connect to the local Milvus server
loop_continue = True
while loop_continue:
    try:
        connection = connections.connect(
            alias="default", 
            host='34.209.51.63',                # or '0.0.0.0' or 'localhost'
            port='19530'
        )
        # Get server version.
        print(f"Milvus server started: {utility.get_server_version()}")
        loop_continue = False
    except:
        max_retries = 3
        retries = 0
        print("Connection to Milvus server failed. Retrying...")
        asyncio.sleep(1)
        retries += 1
        if retries >= max_retries:
            print("Max retries reached. Exiting...")
            loop_continue = False


EMBEDDING_DIM = 1024
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
paper_collection = Collection("paper_chunks")
ref_collection = Collection("ref_chunks")


def encode_pdf_and_get_split_documents(paper_path, chunk_size=1000, chunk_overlap=200) -> List[str]:
    # Load PDF documents
    loader = PyPDFLoader(paper_path)
    documents = loader.load()

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len
    )
    texts = text_splitter.split_documents(documents)
    cleaned_texts = [doc.page_content.replace('\t', ' ') for doc in texts]
    return cleaned_texts


async def fetch_with_retries(client: httpx.AsyncClient, url: str, json_data: dict, retries: int = 3) -> httpx.Response:
    attempt = 0
    while attempt < retries:
        try:
            response = await client.post(url, json=json_data)
            response.raise_for_status()  # Raises HTTPError for bad responses
            return response
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            attempt += 1
            if attempt >= retries:
                raise e
            print(f"Attempt {attempt} failed: {e}. Retrying...")
            await asyncio.sleep(1)  # Exponential backoff could be added here


async def get_dense_vectors(list_of_documents: List[str]) -> List[List[float]]:
    docs = [doc for doc in list_of_documents] 
    slice_size = 10
    tasks = []
    dense_vectors = []

    async with httpx.AsyncClient(timeout=120.0) as client:
        for i in range(0, len(docs), slice_size):
            sliced_docs = docs[i:i + slice_size]
            tasks.append(fetch_with_retries(client, "http://34.209.51.63:8003/compute-embedding/", {"request_id": i, "text_list": sliced_docs}))

        responses = await asyncio.gather(*tasks, return_exceptions=True)        # run tasks and gather the results of the tasks

        for idx, response in enumerate(responses):
            doc_count = idx * slice_size
            print(f"Response: {response}")
            if isinstance(response, Exception) or response.status_code != 200:
                dense_vectors.extend([[0.0] * EMBEDDING_DIM for _ in range(len(docs[doc_count:doc_count + slice_size]))])
                print(f"Error computing embedding for docs {doc_count}-{doc_count + slice_size-1}. Returned 0-vectors.")
            else:
                dense_vectors.extend(response.json()["embeddings"])
                print(f"Dense_vectors {doc_count}-{doc_count + slice_size-1} computed successfully")

    return dense_vectors


def get_sparse_vectors(list_of_documents: List[str]) -> List[Dict]:
    sparse_vectors = []
    docs = [doc for doc in list_of_documents]
    sparse_embedding_func = BM25SparseEmbedding(corpus=docs)
    for i, doc in enumerate(docs):
        sparse_vectors.append(sparse_embedding_func.embed_query(doc))
    return sparse_vectors


async def index_paper_chunks(pdf_text, paper_uuid):
    cleaned_texts = encode_pdf_and_get_split_documents(pdf_text, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    dense_vectors = await get_dense_vectors(cleaned_texts)
    sparse_vectors = get_sparse_vectors(cleaned_texts)
    print(f"Number of dense vectors: {len(dense_vectors)}")
    print(f"Number of sparse vectors: {len(sparse_vectors)}")
    records = [        
        {
            "doc": doc,
            "sparse_vector": sparse_vectors[i],
            "dense_vector": dense_vectors[i],
            "user_id": str(paper_uuid),
            "paper_doi": "",
            "paper_arxiv_id": "",
            "paper_title": "",
        }
        for i, doc in enumerate(cleaned_texts)
    ]

    # Insert the record into Milvus DB
    try:
        paper_collection.insert(records)                          
        paper_collection.flush()                                  # Flush the collection to ensure data is saved
        print("Data inserted successfully into paper chunks collection.")
    except Exception as e:
        print(f"Error inserting data into paper chunks collectio: {str(e)}")



async def index_references(reference_df):
    abstracts = reference_df['abstract'].tolist()
    cleaned_abstracts = [abstract.replace("\t", " ") if abstract else "" for abstract in abstracts]
    dense_vectors = await get_dense_vectors(cleaned_abstracts)
    records = []
    for i, (_, row) in enumerate(reference_df.iterrows()):
        record = {
            "cite_id": row['cite_id'],
            "title": row['res_title'],
            "url": row['URL'],
            "abstract": cleaned_abstracts[i],
            "abstract_dense_vector": dense_vectors[i],
        }
        records.append(record)

    # Insert the record into Milvus DB
    try:
        ref_collection.insert(records)                          
        ref_collection.flush()                                  # Flush the collection to ensure data is saved
        print("Data inserted successfully into ref chunks collection.")
    except Exception as e:
        print(f"Error inserting data into ref chunks collection: {str(e)}")