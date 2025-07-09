import flet as ft
from views.login_view import LoginView
from views.register_view import RegisterView
from views.menu_view import MenuView
from views.product_detail_view import ProductDetailView

def main(page: ft.Page):
    page.title = "Kstore"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#f0f2f5"
    page.window.resizable = True

    def route_change(route):
        page.controls.clear()
        page.appbar = None
        page.navigation_bar = None

        if route.startswith("/product/"):
            try:
                product_id = int(route.split("/")[-1])
                ProductDetailView(page, product_id)
            except (ValueError, IndexError):
                page.go("/menu")
        elif route == "/login":
            LoginView(page, go_to_route)
        elif route == "/register":
            RegisterView(page, go_to_route)
        elif route.startswith("/menu"):
            user_data = getattr(page, 'user_data', None)
            MenuView(page, go_to_route, user_data)
        else:
            LoginView(page, go_to_route)

    def go_to_route(route, user_data=None):
        if user_data:
            page.user_data = user_data
        page.go(route)

    page.on_route_change = lambda e: route_change(page.route)
    initial_route = page.route if page.route else "/login"
    page.go(initial_route)

if __name__ == "__main__":
    ft.app(target=main)