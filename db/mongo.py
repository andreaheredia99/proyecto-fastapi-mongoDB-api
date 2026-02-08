# importamos la libreria asincrona de pymongo para trabajar con mongo en fastapi
import motor.motor_asyncio
import os
from dotenv import load_dotenv

# cargamos la variables de entorno
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB")


# cargamos el client de mongo asincrono
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB_NAME]


# cargamos la coleccion de libros de nuestra booksdb
books_collection = db["books"]
# si tuvieramos mas colecciones las cargariamos aqui
# ej. users_collection = db['users']
