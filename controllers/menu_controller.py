# controllers/menu_controller.py

import flet as ft
import threading
import time  # <--- 1. IMPORTA LA LIBRERÍA 'time'

from models.menu_model import Database
PURPLE = "#6A0DAD"

class MenuController:
    # ... (el __init__ y el main se quedan igual) ...
    def __init__(self):
        self.db = Database()
        self.view = None
        self.all_products = []

    def main(self):
        self.view.show_preloader(True)
        thread = threading.Thread(target=self._load_data_in_background)
        thread.start()
    
    def _load_data_in_background(self):
        try:
            print("Hilo iniciado. Simularé una espera de 1 segundo...")
            time.sleep(1) # <--- 2. AÑADE ESTE RETRASO ARTIFICIAL

            if not self.db.connect():
                raise ConnectionError("La conexión a la base de datos devolvió False.")

            self.all_products = self.db.get_all_products()
            self.view.update_view(self.all_products)

        except Exception as e:
            print(f"Error en el hilo de carga de datos: {e}")
            self.view.show_db_error()

        finally:
            self.view.show_preloader(False)
            print("Hilo finalizado. El preloader debería ocultarse.")

    # ... (el resto de los métodos search_products y add_to_cart se quedan igual) ...
    def search_products(self, query: str):
        if not query:
            self.view.update_view(self.all_products)
            return

        query_lower = query.lower()
        filtered_products = [
            p for p in self.all_products
            if query_lower in p.get('nombre', '').lower()
        ]
        self.view.update_view(filtered_products)

    def add_to_cart(self, product_data):
        product_name = product_data.get('nombre', 'Producto')
        print(f"Controlador: Agregando '{product_name}' al carrito.")

        if self.view and self.view.page:
            add_snack = ft.SnackBar(
                content=ft.Text(f"'{product_name}' agregado al carrito!"),
                bgcolor=PURPLE,
                duration=2000
            )
            self.view.page.overlay.append(add_snack)
            add_snack.open = True
            self.view.page.update()