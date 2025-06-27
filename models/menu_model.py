# menu_model.py

class MenuModel:
    def __init__(self):
        self.current_user = None
        self.menu_items = [
            {"name": "Álbum BTS - 'Map of the Soul: 7'", "category": "álbumes"},
            {"name": "Lightstick BLACKPINK", "category": "merchandising"},
            {"name": "Póster Stray Kids", "category": "posters"},
            {"name": "Photocard TWICE", "category": "photocards"}
        ]
        self.discounts = [
            {"title": "10% OFF", "description": "En álbumes seleccionados"},
            {"title": "Envío gratis", "description": "En compras mayores a $50"},
            {"title": "Regalo sorpresa", "description": "Por la compra de cualquier lightstick"}
        ]

    def set_current_user(self, user_data):
        # Guarda los datos del usuario actual
        self.current_user = user_data

    def get_current_user(self):
        # Retorna los datos del usuario actual
        return self.current_user

    def clear_current_user(self):
        # Limpia los datos del usuario actual
        self.current_user = None

    def get_menu_items(self):
        # Retorna los elementos del menú (alias antiguo)
        return self.menu_items

    def get_products(self):
        # Alias para que funcione con la vista de Kstore
        return self.menu_items

    def get_discounts(self):
        # Retorna los descuentos disponibles
        return self.discounts
