import json
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="FastAPIPractice",
    description="First FastAPI application",
    docs_url="/docs",
    redoc_url="/redoc"
)

def load_data():
    with open("src/fastapiprac/data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open("src/fastapiprac/data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()

class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    genre: str
    price: float
    in_stock: bool

@app.get("/books", response_model=list[Book])
async def get_books():
    return data["books"]

@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    for book in data["books"]:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books", response_model=Book)
async def add_book(book: Book):
    for existing_book in data["books"]:
        if existing_book["id"] == book.id:
            raise HTTPException(status_code=400, detail="Book with this ID already exists")
    
    data["books"].append(book.model_dump())
    save_data(data)
    return book

@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, book: Book):
    for i, existing_book in enumerate(data["books"]):
        if existing_book["id"] == book_id:
            updated_book = book.model_dump()
            updated_book["id"] = book_id
            data["books"][i] = updated_book
            save_data(data)
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i, book in enumerate(data["books"]):
        if book["id"] == book_id:
            deleted_book = data["books"].pop(i)
            save_data(data)
            return {"message": "Book deleted successfully", "book": deleted_book}
    raise HTTPException(status_code=404, detail="Book not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)