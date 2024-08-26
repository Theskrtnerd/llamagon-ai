from pydantic import BaseModel

class URLInput(BaseModel):
    url: str