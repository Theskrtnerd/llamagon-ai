import pymilvus
from pymilvus.model.hybrid import BGEM3EmbeddingFunction
import fastapi
import torch
from fastapi import FastAPI


print(f"PyMilvus: {pymilvus.__version__}")


app = FastAPI()
# # Initialize torch settings
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"device: {DEVICE}")

# Initialize a Milvus built-in sparse-dense-reranking encoder.
# https://huggingface.co/BAAI/bge-m3
embedding_model = BGEM3EmbeddingFunction(use_fp16=False, device=DEVICE)
EMBEDDING_DIM = embedding_model.dim['dense']
print(f"dense_dim: {EMBEDDING_DIM}")
print(f"sparse_dim: {embedding_model.dim['sparse']}")
print(f"colbert_dim: {embedding_model.dim['colbert_vecs']}")