from pymongo import MongoClient


# Base de datos local
# db_client = MongoClient().local # si no ponemos nada de parámetros, se conecta a local host por defecto.

# Base de datos remota
db_client = MongoClient(
    'mongodb+srv://slowstudent:BqIFpGND9EfmGbzD@cluster0.xgxkxi8.mongodb.net/?retryWrites=true&w=majority').slowstudent
