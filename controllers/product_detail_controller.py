import flet as ft
from models.menu_model import Database

class ProductDetailController:
    def __init__(self, view, product_id):
        self.view = view
        self.product_id = product_id
        self.db = Database()
        self.product_data = None
        self.selected_quantity = 1

    def main(self):
        if self.db.connect():
            self.product_data = self.db.get_product_by_id(self.product_id)
            if self.product_data:
                self.view.display_product(self.product_data)
            else:
                self.view.display_error("Producto no encontrado.")
        else:
            self.view.display_error("Error de conexión a la base de datos.")

    def update_quantity_display(self):
        self.view.quantity_text.value = str(self.selected_quantity)
        self.view.page.update()

    def increment_quantity(self, e):
        stock = self.product_data.get('stock', 0)
        if self.selected_quantity < stock:
            self.selected_quantity += 1
            self.update_quantity_display()

    def decrement_quantity(self, e):
        if self.selected_quantity > 1:
            self.selected_quantity -= 1
            self.update_quantity_display()

    def add_to_cart(self, e):
        product_name = self.product_data.get('nombre', 'Producto')
        snack = ft.SnackBar(
            content=ft.Text(f"{self.selected_quantity} x '{product_name}' agregado al carrito!"),
            bgcolor="#6A0DAD", duration=2000
        )
        self.view.page.overlay.append(snack)
        snack.open = True
        self.view.page.update()