import uuid
import pathlib
import hashlib
import requests
from paper_retriever.constants import SHARED_DATA_DIR




def generate_unique_id(url: str) -> str:
    # Generate a SHA-256 hash of the URL
    hash_object = hashlib.sha256(url.encode())
    unique_id = hash_object.hexdigest()
    return unique_id


def download_pdf(url: str) -> bytes:
    response = requests.get(url)
    if response.status_code != 200 or 'application/pdf' not in response.headers.get('Content-Type', ''):
        return None
    return response.content


def save_pdf(working_dir: str, file_name: str, file: bytes) -> str:
    paper_path = f"{working_dir}/{file_name}"  
    if not pathlib.Path(paper_path).exists():
        with open(paper_path, "wb") as f:
            f.write(file)    
    return paper_path


# def make_working_dir():
#     paper_uuid = uuid.uuid4()
#     working_dir = f"{SHARED_DATA_DIR}/papers/{paper_uuid}"
#     pathlib.Path(working_dir).mkdir(parents=True, exist_ok=True)
#     return working_dir, paper_uuid


def make_working_dir():
    working_dir = f"{SHARED_DATA_DIR}/papers"
    pathlib.Path(working_dir).mkdir(parents=True, exist_ok=True)
    return working_dir


