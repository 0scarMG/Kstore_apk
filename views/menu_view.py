import flet as ft
from controllers.menu_controller import MenuController
from components.store_components import Navbar, StoreLayout, BottomNavBar, FilterBottomSheet

class MenuView:
    def __init__(self, page: ft.Page, go_to_route, user_data=None):
        self.page = page
        self.go_to_route = go_to_route
        self.user_data = user_data
        self.controller = MenuController()
        # Enlazar la vista con el controlador
        self.controller.view = self 
        self.store_layout = StoreLayout(self.controller, self.page)
        self.navbar = Navbar(self.controller, on_filter_click=self.open_filters)
        self.bottom_nav = BottomNavBar(self.go_to_route)
        self.filter_bottomsheet = None
        self.build()

    def open_filters(self, e):
        try:
            initial_filter_data = self.controller.get_initial_filter_data()
            self.filter_bottomsheet = FilterBottomSheet(
                controller=self.controller,
                categories=initial_filter_data.get('categories', []),
                max_price=initial_filter_data.get('max_price', 1000),
            )
            self.page.overlay.append(self.filter_bottomsheet)
            self.filter_bottomsheet.open = True
            self.page.update()
        except Exception as ex:
            print(f"Error al abrir filtros: {ex}")

    def build(self):
        self.page.appbar = self.navbar
        self.page.navigation_bar = self.bottom_nav
        self.page.scroll = ft.ScrollMode.ADAPTIVE
        self.page.add(self.store_layout.build())
        
        if self.user_data:
            welcome_name = self.user_data.get('usuario', 'Usuario')
            welcome_snack = ft.SnackBar(
                content=ft.Text(f"¡Bienvenido de vuelta, {welcome_name}!"),
                duration=3000, bgcolor=ft.Colors.PURPLE_700, action="OK"
            )
            self.page.overlay.append(welcome_snack)
            welcome_snack.open = True
        
        self.page.update()
        self.controller.main()