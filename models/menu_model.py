import os
import pymongo
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

class Database:
    def __init__(self):
        load_dotenv()
        self.mongo_uri = os.getenv("MONGO_URI")
        self.client = None
        self.db = None
        self.products_collection = None

    def connect(self):
        if not self.mongo_uri:
            print("Error: La variable de entorno MONGO_URI no está configurada.")
            return False
        try:
            self.client = pymongo.MongoClient(self.mongo_uri)
            self.client.admin.command('ping')
            print("Conexión a MongoDB exitosa.")
            self.db = self.client["kstoredb"]
            self.products_collection = self.db.products
            self._seed_database()
            return True
        except ConnectionFailure as e:
            print(f"Error de conexión a MongoDB: {e}")
            return False
        except Exception as e:
            print(f"Ocurrió un error inesperado al conectar: {e}")
            return False

    def get_all_products(self):
        if self.products_collection is None:
            return []
        try:
            return list(self.products_collection.find())
        except Exception as e:
            print(f"Error al obtener productos: {e}")
            return []

    def get_product_by_id(self, product_id: int):
        if self.products_collection is None:
            return None
        try:
            return self.products_collection.find_one({"id": product_id})
        except Exception as e:
            print(f"Error al obtener producto por ID: {e}")
            return None

    def _seed_database(self):
        if self.products_collection is not None and self.products_collection.count_documents({}) == 0:
            print("Base de datos vacía, insertando productos de ejemplo con más detalles...")
            sample_products = [
                {
                    'id': 1, 'nombre': 'BTS - BE', 'precio': 25.99, 'categoria': 'Álbumes',
                    'descripcion': 'El álbum auto-producido de BTS que reflexiona sobre la vida durante la pandemia. Incluye el éxito "Dynamite".',
                    'imagenes_urls': [
                        'https://ibighit.com/bts/images/bts/discography/be/rwM39x2S533aDD1b3p2lBNoG.jpg',
                        'https://m.media-amazon.com/images/I/717Q815UGXL._AC_SL1500_.jpg',
                        'https://m.media-amazon.com/images/I/817A8cI1S6L._AC_SL1500_.jpg'
                    ], 'stock': 100
                },
                {
                    'id': 2, 'nombre': 'BLACKPINK - The Album', 'precio': 22.50, 'categoria': 'Álbumes',
                    'descripcion': 'El esperado primer álbum de estudio de BLACKPINK. Incluye colaboraciones con Selena Gomez y Cardi B.',
                    'imagenes_urls': [
                        'https://upload.wikimedia.org/wikipedia/en/1/1a/Blackpink_-_The_Album.png',
                        'https://m.media-amazon.com/images/I/81acE4A+V-L._AC_SL1500_.jpg'
                    ], 'stock': 80
                },
                {
                    'id': 3, 'nombre': 'Stray Kids - Light Stick', 'precio': 55.00, 'categoria': 'Merchandising',
                    'descripcion': 'La nueva versión del light stick oficial de Stray Kids. Indispensable para cualquier fan en conciertos.',
                    'imagenes_urls': [
                        'https://cnjenter.com/cdn/shop/products/stray-kids-official-light-stick-ver.2--cn-j-entertainment-2_1024x.jpg?v=1685328236'
                    ], 'stock': 0
                }
            ]
            try:
                self.products_collection.insert_many(sample_products)
                print(f"{len(sample_products)} productos de ejemplo insertados.")
            except Exception as e:
                print(f"Error al insertar productos de ejemplo: {e}")