# menu_controller.py
import flet as ft
from models.menu_model import MenuModel

class MenuController:
    def __init__(self, view):
        self.view = view
        self.model = MenuModel()
        self.current_user = None
    
    def set_user(self, user_data):
        #Establece el usuario logueado
        self.current_user = user_data
        self.model.set_current_user(user_data)
    
    def handle_navigation(self, selected_index):
        #Maneja los cambios de navegación
        self.view.update_content_by_index(selected_index)
    
    def get_user_info(self):
        #Obtiene información del usuario actual
        return self.model.get_current_user()
    
    def logout(self):
        #Cierra sesión del usuario
        self.current_user = None
        self.model.clear_current_user()
        # Redirigir al login
        self.view.go_to_route("/login")