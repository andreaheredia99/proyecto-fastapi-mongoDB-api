from pydantic import BaseModel
from typing import Optional


class BookCreate(BaseModel):
    title: str
    author: str
    year: int
    pages: Optional[int]
    # campo opcional


class Book(BookCreate):
    id: str
