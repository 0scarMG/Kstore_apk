# model.py
import os
import pymongo
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

class Database:
    """
    Gestiona la conexión y las operaciones con la base de datos MongoDB.
    """
    def __init__(self):
        """Carga las variables de entorno para la conexión."""
        load_dotenv()
        self.mongo_uri = os.getenv("MONGO_URI")
        self.client = None
        self.db = None
        self.products_collection = None

    def connect(self):
        """
        Intenta conectarse a la base de datos MongoDB.
        Devuelve True si la conexión es exitosa, False en caso contrario.
        """
        if not self.mongo_uri:
            print("Error: La variable de entorno MONGO_URI no está configurada.")
            return False
        try:
            self.client = pymongo.MongoClient(self.mongo_uri)
            # El comando 'ping' confirma una conexión exitosa.
            self.client.admin.command('ping')
            print("Conexión a MongoDB exitosa.")
            self.db = self.client.get_default_database()
            self.products_collection = self.db.products
            self._seed_database() # Poblar con datos de ejemplo si es necesario
            return True
        except ConnectionFailure as e:
            print(f"Error de conexión a MongoDB: {e}")
            return False
        except Exception as e:
            print(f"Ocurrió un error inesperado al conectar: {e}")
            return False

    def get_all_products(self):
        """Obtiene todos los productos de la colección."""
        if not self.products_collection:
            return []
        try:
            return list(self.products_collection.find())
        except Exception as e:
            print(f"Error al obtener productos: {e}")
            return []

    def search_products(self, query):
        """
        Busca productos por nombre o categoría usando una expresión regular (case-insensitive).
        """
        if not self.products_collection:
            return []
        try:
            # Búsqueda case-insensitive en los campos 'nombre' y 'categoria'
            return list(self.products_collection.find({
                "$or": [
                    {"nombre": {"$regex": query, "$options": "i"}},
                    {"categoria": {"$regex": query, "$options": "i"}}
                ]
            }))
        except Exception as e:
            print(f"Error al buscar productos: {e}")
            return []
    
    def _seed_database(self):
        """
        Puebla la base de datos con datos de ejemplo si la colección 'products' está vacía.
        Esto es útil para la primera ejecución.
        """
        if self.products_collection is not None and self.products_collection.count_documents({}) == 0:
            print("Base de datos vacía, insertando productos de ejemplo...")
            sample_products = [
                {'id': 1, 'nombre': 'BTS - BE', 'precio': 25.99, 'categoria': 'Álbumes', 'imagen_url': 'https://ibighit.com/bts/images/bts/discography/be/rwM39x2S533aDD1b3p2lBNoG.jpg', 'stock': 100},
                {'id': 2, 'nombre': 'BLACKPINK - The Album', 'precio': 22.50, 'categoria': 'Álbumes', 'imagen_url': 'https://upload.wikimedia.org/wikipedia/en/1/1a/Blackpink_-_The_Album.png', 'stock': 80},
                {'id': 3, 'nombre': 'Stray Kids - Light Stick', 'precio': 55.00, 'categoria': 'Merchandising', 'imagen_url': 'https://cnjenter.com/cdn/shop/products/stray-kids-official-light-stick-ver.2--cn-j-entertainment-2_1024x.jpg?v=1685328236', 'stock': 50},
                {'id': 4, 'nombre': 'TWICE - Formula of Love', 'precio': 24.00, 'categoria': 'Álbumes', 'imagen_url': 'https://upload.wikimedia.org/wikipedia/en/5/52/Twice_-_Formula_of_Love.png', 'stock': 120},
                {'id': 5, 'nombre': 'TXT - The Chaos Chapter: FREEZE', 'precio': 21.99, 'categoria': 'Álbumes', 'imagen_url': 'https://ibighit.com/txt/images/txt/discography/the-chaos-chapter-freeze/EBlD2sIW2E4y_M52ridwMh5k.jpg', 'stock': 90},
                {'id': 6, 'nombre': 'NCT - Universe Hoodie', 'precio': 45.00, 'categoria': 'Merchandising', 'imagen_url': 'https://m.media-amazon.com/images/I/61t-XGz-69L._AC_SY550_.jpg', 'stock': 30},
                {'id': 7, 'nombre': 'Red Velvet - Queendom (Oferta)', 'precio': 18.99, 'categoria': 'Ofertas', 'imagen_url': 'https://upload.wikimedia.org/wikipedia/en/thumb/e/e3/Red_Velvet_-_Queendom.png/220px-Red_Velvet_-_Queendom.png', 'stock': 200},
                {'id': 8, 'nombre': 'ATEEZ - Treasure EP.Fin: All to Action', 'precio': 23.50, 'categoria': 'Álbumes', 'imagen_url': 'https://upload.wikimedia.org/wikipedia/en/e/e1/ATEEZ_-_Treasure_EP.Fin_-_All_to_Action.png', 'stock': 75}
            ]
            try:
                self.products_collection.insert_many(sample_products)
                print(f"{len(sample_products)} productos de ejemplo insertados.")
            except Exception as e:
                print(f"Error al insertar productos de ejemplo: {e}")

