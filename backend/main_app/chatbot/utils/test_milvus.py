import asyncio
import requests
import pymilvus
from pymilvus import (
    MilvusClient, Collection, utility, connections,
)
print(f"Pymilvus: {pymilvus.__version__}")


# Connect to the local server
while True:
    try:
        connection = connections.connect(
            alias="default", 
            host='34.209.51.63',                # or '0.0.0.0' or 'localhost'
            port='19530'
        )
        # Get server version.
        print(f"Milvus server instantiated: {utility.get_server_version()}")
        # Check the collection using MilvusClient.
        milvus_client = MilvusClient(connections=connection)
        break
    except:
        print("Connection to Milvus server failed. Retrying...")
        asyncio.sleep(1)
        continue


COLLECTION_NAME = "paper_chunks"
EMBEDDING_DIM = 1024

collections = utility.list_collections()
print(f"Current collections: {collections}")
collection = Collection(COLLECTION_NAME)


# Step 1: call to port 8003 to compute the chunk's embedding
doc = "Sample document text goes here..."
response = requests.post("http://localhost:8003/compute-embedding", json={"text_list": [doc]})
if response.status_code == 200:
    embedding = response.json()["embeddings"][0]
    print(f"Embedding computed successfully: {embedding[:10]}...")
else:
    embedding = [0.0] * EMBEDDING_DIM
    print(f"Error computing embedding: {response.json()}")


# Step 2: insert the chunk record into the Milvus collection
records = [
    {
        "doc": "Sample document text goes here...",
        "sparse_vector": {0: 1.0, 100: 0.5, 200: 0.75},
        "dense_vector": embedding,
        "user_id": 123,
        "paper_id": 456,
        "paper_doi": "10.1234/example-doi",
        "paper_arxiv_id": "arXiv:1234.5678",
        "paper_title": "Sample Paper Title",
        "reference_ids": [789, 1011, 1213]
    }
]


try:
    collection.insert(records)                          
    collection.flush()                                  # Flush the collection to ensure data is saved
    print("Data inserted successfully.")
except Exception as e:
    print(f"Error inserting data: {str(e)}")