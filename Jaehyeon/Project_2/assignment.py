from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(title='id is not needed')
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1899, lt=2024)

    class Config:
        schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'codingwithroby',
                'description': 'A new description of a book',
                'rating': 5,
                'published_date': 2021
            }
        }

BOOKS: list[Book] = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2000),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 1957),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2015),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2023),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 1901),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 1998)
]



@app.get("/books/published")
async def read_books_by_publish_date(published_date: int = Query(gt=1899, lt=2024)):
    return list(filter(lambda x: x.published_date == published_date, BOOKS))