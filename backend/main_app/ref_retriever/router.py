from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.params import Query
import requests
import os


router = APIRouter(
    prefix = '/ref_retriever',
    tags = ['ref_retriever'],
)


@router.get("/")
def read_root():
    return JSONResponse(content={"message": "Welcome to the reference search API"})


@router.get("/search")
def search():
    pass