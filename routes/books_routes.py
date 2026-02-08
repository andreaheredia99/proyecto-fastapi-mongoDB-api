from fastapi import APIRouter
from controllers import books_controllers
from models.book_models import BookCreate

router = APIRouter()


@router.get("/", status_code=200)
async def get_book_list():
    return await books_controllers.get_book_list()


@router.get("/{id_book}", status_code=200)
async def get_book_by_id(id_book: str):
    return await books_controllers.get_book_by_id(id_book)


@router.delete("/{id_book}", status_code=200)
async def delete_book_by_id(id_book: str):
    return await books_controllers.delete_book_id(id_book)


@router.post("/", status_code=200)
async def create_book(book: BookCreate):
    return await books_controllers.create_book(book)


@router.put("/{id_book}", status_code=200)
async def update_book_by_id(id_book: str, book: BookCreate):
    return await books_controllers.update_book_by_id(id_book, book)
