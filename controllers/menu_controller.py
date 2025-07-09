import flet as ft
import threading
from models.menu_model import Database

PURPLE = "#6A0DAD"

class MenuController:
    def __init__(self):
        self.db = Database()
        self.view = None
        self.all_products = []

    def main(self):
        if self.view:
            self.view.show_preloader(True)
        thread = threading.Thread(target=self._load_data_in_background)
        thread.start()
    
    def _load_data_in_background(self):
        try:
            if not self.db.connect():
                raise ConnectionError("La conexión a la base de datos falló.")
            self.all_products = self.db.get_all_products()
            if self.view:
                self.view.update_view(self.all_products)
        except Exception as e:
            print(f"Error en el hilo de carga de datos: {e}")
            if self.view:
                self.view.show_db_error()
        finally:
            if self.view:
                self.view.show_preloader(False)
    
    def view_product_details(self, product_data):
        print(f"Click en producto: {product_data.get('nombre', 'Sin nombre')}")
        product_id = product_data.get('id')
        print(f"ID del producto: {product_id}")
        
        if product_id and self.view and hasattr(self.view, 'page'):
            print(f"Navegando a: /product/{product_id}")
            self.view.page.go(f"/product/{product_id}")
        else:
            print(f"Error: No se pudo navegar al producto {product_id}")
            print(f"self.view: {self.view}")
            print(f"Tiene página: {hasattr(self.view, 'page') if self.view else 'No view'}")

    def search_products(self, query: str):
        if not query:
            self.view.update_view(self.all_products)
            return
        query_lower = query.lower()
        filtered_products = [
            p for p in self.all_products if query_lower in p.get('nombre', '').lower()
        ]
        self.view.update_view(filtered_products)

    def add_to_cart(self, product_data):
        product_name = product_data.get('nombre', 'Producto')
        if self.view and self.view.page:
            add_snack = ft.SnackBar(
                content=ft.Text(f"'{product_name}' agregado al carrito!"),
                bgcolor=PURPLE, duration=2000
            )
            self.view.page.overlay.append(add_snack)
            add_snack.open = True
            self.view.page.update()

    def get_initial_filter_data(self):
        try:
            if not self.all_products:
                return {'categories': [], 'max_price': 1000}
            categories = sorted(list(set(
                p.get('categoria') for p in self.all_products if p.get('categoria')
            )))
            prices = [p.get('precio', 0) for p in self.all_products if isinstance(p.get('precio'), (int, float))]
            max_price = max(prices) if prices else 1000
            return {'categories': categories, 'max_price': float(max_price)}
        except Exception as e:
            print(f"Error al obtener datos iniciales de filtros: {e}")
            return {'categories': [], 'max_price': 1000}

    def apply_filters(self, filters):
        try:
            filtered = self.all_products.copy()
            if filters.get('category'):
                filtered = [p for p in filtered if p.get('categoria') == filters['category']]
            if filters.get('price_range'):
                min_price, max_price = filters['price_range']
                filtered = [p for p in filtered if min_price <= p.get('precio', 0) <= max_price]
            
            sort_by = filters.get('sort_by', 'popularity')
            if sort_by == 'price_asc':
                filtered.sort(key=lambda x: x.get('precio', 0))
            elif sort_by == 'price_desc':
                filtered.sort(key=lambda x: x.get('precio', 0), reverse=True)
            
            self.view.update_view(filtered)
            
            if self.view and self.view.page:
                msg = f"Filtros aplicados: {len(filtered)} productos" if any(filters) else "Filtros limpiados"
                snack = ft.SnackBar(content=ft.Text(msg), bgcolor=PURPLE, duration=2000)
                self.view.page.overlay.append(snack)
                snack.open = True
                self.view.page.update()
        except Exception as e:
            print(f"Error al aplicar filtros: {e}")
            self.view.update_view(self.all_products)