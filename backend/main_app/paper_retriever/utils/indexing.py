from langchain_milvus.utils.sparse import BM25SparseEmbedding
from typing import List, Dict
import asyncio
import httpx
import pymilvus
import nltk
nltk.download('punkt_tab')
from pymilvus import Collection, utility, connections
from paper_retriever.utils.preprocess import encode_pdf_and_get_split_documents


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
summary_collection = Collection("paper_summaries")


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
        sparse_vector = sparse_embedding_func.embed_query(doc)
        for key in sparse_vector:
            if sparse_vector[key] < 0.0:
                sparse_vector[key] = 0.0
        sparse_vectors.append(sparse_vector)
    return sparse_vectors


async def index_paper_chunks(url, paper_path):
    cleaned_texts = encode_pdf_and_get_split_documents(paper_path, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    dense_vectors = await get_dense_vectors(cleaned_texts)
    sparse_vectors = get_sparse_vectors(cleaned_texts)
    print(f"Number of dense vectors: {len(dense_vectors)}")
    print(f"Number of sparse vectors: {len(sparse_vectors)}")
    records = [        
        {
            "url": url,
            "doc": doc,
            "sparse_vector": sparse_vectors[i],
            "dense_vector": dense_vectors[i],
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



async def index_references(base_url, reference_df):
    abstracts = reference_df['abstract'].tolist()
    cleaned_abstracts = [abstract.replace("\t", " ") if abstract else "" for abstract in abstracts]
    dense_vectors = await get_dense_vectors(cleaned_abstracts)
    records = []
    for i, (_, row) in enumerate(reference_df.iterrows()):
        record = {
            "base_url": base_url,
            "cite_id": row['cite_id'],
            "url": row['URL'],
            "title": row['res_title'],
            "arxiv_id": row['arxiv_id'],
            "abstract": cleaned_abstracts[i],
            "abstract_dense_vector": dense_vectors[i],
        }
        print(f"cite_id: {row['cite_id']}")
        print(f"title: {row['res_title']}")
        print(f"url: {row['URL']}")
        print(f"abstract: {cleaned_abstracts[i]}")
        records.append(record)

    # Insert the record into Milvus DB
    if records == []:
        print("No records to insert into ref chunks collection.")
    else:
        try:
            ref_collection.insert(records)                          
            ref_collection.flush()                                  # Flush the collection to ensure data is saved
            print("Data inserted successfully into ref chunks collection.")
        except Exception as e:
            print(f"Error inserting data into ref chunks collection: {str(e)}")


async def index_summary(url, summary):
    try:
        summary_collection.insert([
            {
                "url": url,
                "user_id": "",
                "paper_doi": url,
                "paper_arxiv_id": "",
                "paper_title": "",
                "summary": summary,
                "summary_sparse_vector": get_sparse_vectors([summary])[0],
            }
        ])
        print("Data inserted successfully into paper summaries collection.")
    except Exception as e:
        print(f"Error inserting data into paper summaries collection: {str(e)}")
