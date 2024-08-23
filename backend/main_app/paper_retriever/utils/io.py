import uuid
import pathlib
from paper_retriever.constants import SHARED_DATA_DIR
from fastapi import UploadFile, File


def is_paper(pdf_text: str) -> bool:
    pass


def save_pdf(working_dir: str, file: UploadFile = File(...)) -> str:
    paper_path = f"{working_dir}/{file.filename}"
    with open(paper_path, "wb") as f:
        f.write(file.file.read())
    return paper_path


def make_working_dir():
    paper_uuid = uuid.uuid4()
    working_dir = f"{SHARED_DATA_DIR}/papers/{paper_uuid}"
    pathlib.Path(working_dir).mkdir(parents=True, exist_ok=True)
    return working_dir