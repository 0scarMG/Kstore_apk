import flet as ft
from views.login_view import LoginView
from views.register_view import RegisterView
from views.menu_view import MenuView

def main(page: ft.Page):
    page.title = "Kstore"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 411 
    page.window.height = 731
    page.bgcolor = "#f0f2f5"
    page.window.resizable = True

    def route_change(route):
        page.controls.clear()  # Limpia los controles actuales
        page.navigation_bar = None  # Limpia la barra de navegación si existe

        if route == "/login":
            LoginView(page, go_to_route)
        elif route == "/register":
            RegisterView(page, go_to_route)
        elif route.startswith("/menu"):
            # Extraer datos de usuario de la ruta si están presentes
            # Por ejemplo: /menu?user_data=...
            user_data = getattr(page, 'user_data', None)
            MenuView(page, go_to_route, user_data)
        else:
            LoginView(page, go_to_route)  # Ruta por defecto

        page.update()

    def go_to_route(route, user_data=None):
        # Guardar datos de usuario en la página si se proporcionan
        if user_data:
            page.user_data = user_data
        page.go(route)


    page.on_route_change = lambda e: route_change(page.route)

    # Inicializa la ruta actual
    route_change(page.route)

if __name__ == "__main__":
    ft.app(target=main)
