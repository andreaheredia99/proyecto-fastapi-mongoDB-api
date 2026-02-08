from fastapi import FastAPI
from routes import books_routes

app = FastAPI()

# Ruta de acceso a los libros
app.include_router(books_routes.router, prefix="/books", tags=["Books"])
