from langchain.document_loaders import  PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_milvus.utils.sparse import BM25SparseEmbedding
from typing import List, Dict
import asyncio
import httpx


COLLECTION_NAME = "paper_chunks"
EMBEDDING_DIM = 1024
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def replace_t_with_space(list_of_documents: List[Document]) -> List[Document]:
    for doc in list_of_documents:
        doc.page_content = doc.page_content.replace('\t', ' ')  
    return list_of_documents


def encode_pdf_and_get_split_documents(path, chunk_size=1000, chunk_overlap=200) -> List[Document]:
    # Load PDF documents
    loader = PyPDFLoader(path)
    documents = loader.load()

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len
    )
    texts = text_splitter.split_documents(documents)
    cleaned_texts = replace_t_with_space(texts)

    print()
    print(f"Number of documents: {len(cleaned_texts)}")
    for i, doc in enumerate(cleaned_texts):
        print()
        # print(f"Document {i}: {doc.page_content}...")
        if i == 4:
            break

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


async def get_dense_vectors(list_of_documents: List[Document]) -> List[List[float]]:
    docs = [doc.page_content for doc in list_of_documents] 
    slice_size = 10
    tasks = []
    dense_vectors = []

    async with httpx.AsyncClient(timeout=60.0) as client:
        for i in range(0, len(docs), slice_size):
            sliced_docs = docs[i:i + slice_size]
            request_id = i
            tasks.append(fetch_with_retries(client, "http://34.209.51.63:8003/compute-embedding/", {"request_id": request_id, "text_list": sliced_docs}))

        responses = await asyncio.gather(*tasks, return_exceptions=True)        # run tasks and gather the results of the tasks
        print(f"Responses: {responses}")
        
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


def get_sparse_vectors(list_of_documents: List[Document]) -> List[Dict]:
    sparse_vectors = []
    docs = [doc.page_content for doc in list_of_documents]
    sparse_embedding_func = BM25SparseEmbedding(corpus=docs)
    for i, doc in enumerate(docs):
        sparse_vectors.append(sparse_embedding_func.embed_query(doc))
        # print()
        print(f"Length of sparse embedding vector for doc {i}: {len(sparse_vectors[i])}")
        # print(f"Sparse embedding computed successfully for doc {i}: {sparse_embedding.keys()}...")
    return sparse_vectors


if __name__ == "__main__":
    cleaned_texts = encode_pdf_and_get_split_documents("./vbs.pdf", CHUNK_SIZE, CHUNK_OVERLAP)
    dense_vectors = asyncio.run(get_dense_vectors(cleaned_texts))
    sparse_vectors = get_sparse_vectors(cleaned_texts)
    print(f"Length of dense_vectors: {len(dense_vectors)}")
    print(f"Length of dense_vectors[0]: {len(dense_vectors[0])}")
    print(f"Length of sparse_vectors: {len(sparse_vectors)}")
    print(f"Length of sparse_vectors[0]: {len(sparse_vectors[0])}")


