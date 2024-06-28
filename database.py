from pymongo import MongoClient
import certifi

MONGO_URI = 'mongodb+srv://engc90:engc1990@cluster0.1vaz5b9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client["dbb_products_app"]
    except ConnectionError:
        print('Error de conexion con la base de Base de datos')
    return db
