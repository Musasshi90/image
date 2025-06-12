from pydantic import BaseModel


class Image(BaseModel):
    id: int = None
    file_name: str
    created_date: str
    url: str
