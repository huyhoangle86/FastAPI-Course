from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

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
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=2000, lt=2029)

    model_config = {
        "json_schema_extra": {
            "example" : {
                "title": "A new book",
                "author": "coding with Lee",
                "description": "A new description of a book",
                "rating" : 5,
                "publish_date": 2022
            }
        }
    }
     

BOOKS = [
    Book(1, 'Computer Science Pro', 'learning with lee', 'A very nice book', 5, 2011),
    Book(2, 'Be Fast with Fast API', 'learning with lee', 'A great book', 5, 2022),
    Book(3, 'Master Endpoints', 'learning with lee', 'A awesome book', 5, 2023),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2011),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2022),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2003)
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')
        
@app.get("/books/",status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

@app.get("/books/publish/",status_code=status.HTTP_200_OK)
async def read_book_by_published_date(published_date: int = Query(gt=2000, lt=2029)):
    book_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            book_to_return.append(book)
    return book_to_return

@app.post("/create_book",status_code=status.HTTP_201_CREATED)
async def create_book(book_request : BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    
    return book


@app.put("/books/update_book",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_change = True
    if not book_change:
        raise HTTPException(status_code=404, detail='Item not found')

@app.delete("/books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_change = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_change = True
            break
    if not book_change:
        raise HTTPException(status_code=404, detail='Item not found')
