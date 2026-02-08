from fastapi import HTTPException

# como vamos a conectarnos con una BBDD Mongo tengo dque importar el fichero de conexion
from db.mongo import books_collection

# id de mongo es alfanumerico es un objeto especial de mongo
from bson import ObjectId
from models.book_models import BookCreate, Book

# vamos a crear funcion cuyo objetivo es montrarme json, pero tenemos objeto de tipo mongo que no son jason tengo que crear un class Book models que me ayude a convertir dichos objetos de mongo python => mongo y vieceversa. Es nuestra funcion de parseo de datos.


def book_helper(book: dict) -> Book:
    return Book(
        id=str(book["_id"]),
        title=book["title"],
        author=book["author"],
        year=book["year"],
        pages=book.get(
            "pages"
        ),  # el metodo get si no existe paginas por que es opcional me devuelve null. no me falla
    )


async def get_book_list():
    try:
        # recuperamos todos los libros de una vez y los parseamos.
        result = await books_collection.find({}).to_list(length=None)
        return [book_helper(item) for item in result]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


async def get_book_by_id(id_book: str):
    try:
        if not ObjectId.is_valid(id_book):
            raise HTTPException(status_code=400, detail="ID del libro no es valido")
        book = await books_collection.find_one({"_id": ObjectId(id_book)})
        if book:
            return book_helper(book)
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


async def delete_book_id(id_book: str):
    try:
        if not ObjectId.is_valid(id_book):
            raise HTTPException(status_code=400, detail="ID del libro no es valido")
        result = await books_collection.delete_one({"_id": ObjectId(id_book)})
        if not result.deleted_count == 1:
            raise HTTPException(
                status_code=409, detail="No se ha borrado el libro, intentalo de nuevo"
            )
        return {"msg": f"Libro con id {id_book} borrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


async def create_book(book: BookCreate):
    try:
        # tenemos un modelo de tipo book -> dict = basemodel tiene un metodo que me permite transformar de book a diccionario se llama model_dump()
        new_book = book.model_dump()
        result = await books_collection.insert_one(new_book)
        created_book = await books_collection.find_one({"_id": result.inserted_id})
        return book_helper(created_book)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


async def update_book_by_id(id_book: str, book: BookCreate):
    try:
        if not ObjectId.is_valid(id_book):
            raise HTTPException(status_code=400, detail="ID del libro no es valido")
        result = await books_collection.update_one(
            {"_id": ObjectId(id_book)},
            {"$set": book.model_dump()},
            # $set selecciona todos los campos, sin necesidad de escribirlos
        )
        if result.modified_count == 0:
            return None
        update = await books_collection.find_one({"_id": ObjectId(id_book)})
        return book_helper(update)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
