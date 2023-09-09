from fastapi import FastAPI


### data
BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


### fastapi
app = FastAPI()

@app.get("/books/{author}/")
async def read_books(author: str):
    return list(filter(lambda book: book.get("author").casefold() == author.casefold(), BOOKS))

@app.get("/books/author/")
async def read_books_by_query(author: str):
    return list(filter(lambda book: book.get("author").casefold() == author.casefold(), BOOKS))