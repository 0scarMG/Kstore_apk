import flet as ft
from views.login_view import LoginView
from views.register_view import RegisterView

def main(page: ft.Page):
    page.title = "Kstore"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 411 
    page.window.height = 731
    page.bgcolor = "#f0f2f5"
    page.window.resizable = True

    def route_change(route):
        page.controls.clear()  # Limpia los controles actuales

        if route == "/login":
            LoginView(page, go_to_route)
        elif route == "/register":
            RegisterView(page, go_to_route)
        else:
            LoginView(page, go_to_route)  # Ruta por defecto

        page.update()

    def go_to_route(route):
        page.go(route)

    page.on_route_change = lambda e: route_change(page.route)

    # Inicializa la ruta actual
    route_change(page.route)

if __name__ == "__main__":
    ft.app(target=main)
