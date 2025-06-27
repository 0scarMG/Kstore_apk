# menu_view.py
import flet as ft
from controllers.menu_controller import MenuController  # Corrige el import relativo

class MenuView:
    def __init__(self, page: ft.Page, go_to_route, user_data=None):
        self.page = page
        self.go_to_route = go_to_route
        self.controller = MenuController(self)

        if user_data:
            self.controller.set_user(user_data)

        self._setup_page()
        self.content_container = ft.Container(expand=True, padding=0)
        self._create_navigation_bar()
        self._update_content(0)
        self.page.add(self.content_container)

    def _setup_page(self):
        self.page.title = "KStore"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.bgcolor = ft.Colors.GREY_100
        self.page.padding = 0
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def _create_navigation_bar(self):
        self.nav_bar = ft.NavigationBar(
            bgcolor=ft.Colors.WHITE,
            selected_index=0,
            elevation=10,
            shadow_color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
            indicator_color=ft.Colors.with_opacity(0.1, ft.Colors.PINK_700),
            on_change=self._on_navigation_change,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Inicio"),
                ft.NavigationBarDestination(icon=ft.Icons.SHOPPING_BAG_OUTLINED, selected_icon=ft.Icons.SHOPPING_BAG, label="Tienda"),
                ft.NavigationBarDestination(icon=ft.Icons.LOCAL_OFFER_OUTLINED, selected_icon=ft.Icons.LOCAL_OFFER, label="Ofertas"),
                ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, selected_icon=ft.Icons.PERSON, label="Perfil")
            ]
        )
        self.page.navigation_bar = self.nav_bar

    def _on_navigation_change(self, e):
        self._update_content(e.control.selected_index)

    def _update_content(self, index):
        content_map = {
            0: self._create_home_content,
            1: self._create_store_content,
            2: self._create_discounts_content,
            3: self._create_profile_content
        }
        self.content_container.content = content_map.get(index, self._create_home_content)()
        self.page.update()

    def _create_home_content(self):
        user_info = self.controller.get_user_info()
        user_name = user_info.get('Nombre', 'Usuario') if user_info else 'Usuario'

        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text(f"\u2728 Bienvenido a KStore, {user_name}!", size=26, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text("Descubre lo mejor del mundo K-pop.", size=16, color=ft.Colors.WHITE70)
                ], alignment=ft.MainAxisAlignment.CENTER),
                padding=40,
                gradient=ft.LinearGradient(colors=[ft.Colors.PINK_800, ft.Colors.PINK_400], begin=ft.alignment.top_left, end=ft.alignment.bottom_right),
                border_radius=ft.border_radius.only(bottom_left=25, bottom_right=25)
            ),
            ft.Container(
                content=ft.Text("Nuevos lanzamientos y mercancía exclusiva.", size=18),
                padding=20
            )
        ], scroll=ft.ScrollMode.AUTO)

    def _create_store_content(self):
        products = self.controller.model.get_products()

        return ft.Column([
            ft.Container(
                content=ft.Text("Tienda K-pop", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                padding=30,
                bgcolor=ft.Colors.PINK_700,
                alignment=ft.alignment.center,
                border_radius=ft.border_radius.only(bottom_left=25, bottom_right=25)
            ),
            ft.GridView(
                controls=[self._create_product_card(p) for p in products],
                padding=20,
                runs_count=2,
                max_extent=200,
                child_aspect_ratio=0.8,
                spacing=10,
                run_spacing=10
            )
        ], scroll=ft.ScrollMode.AUTO)

    def _create_product_card(self, product):
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ALBUM, size=50, color=ft.Colors.PINK_700),
                    ft.Text(product["name"], size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(product["category"], size=12, color=ft.Colors.GREY)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                alignment=ft.alignment.center,
                on_click=lambda e: print(f"Producto: {product['name']}")
            ),
            elevation=5
        )

    def _create_discounts_content(self):
        discounts = self.controller.model.get_discounts()

        return ft.Column([
            ft.Container(
                content=ft.Text("Ofertas Especiales", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                padding=30,
                bgcolor=ft.Colors.PINK_700,
                alignment=ft.alignment.center,
                border_radius=ft.border_radius.only(bottom_left=25, bottom_right=25)
            ),
            ft.ListView(
                controls=[self._create_discount_card(d) for d in discounts],
                padding=20,
                spacing=10
            )
        ], scroll=ft.ScrollMode.AUTO)

    def _create_discount_card(self, discount):
        return ft.Card(
            content=ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.LOCAL_OFFER, size=40, color=ft.Colors.PINK_700),
                    ft.Column([
                        ft.Text(discount["title"], size=20, weight=ft.FontWeight.BOLD),
                        ft.Text(discount["description"], size=16)
                    ], spacing=5)
                ], spacing=15),
                padding=20
            ),
            elevation=3
        )

    def _create_profile_content(self):
        user_info = self.controller.get_user_info()

        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.PERSON, size=80, color=ft.Colors.WHITE),
                    ft.Text(user_info.get('Nombre', 'Usuario'), size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text("Mi Perfil", size=16, color=ft.Colors.WHITE70)
                ], alignment=ft.MainAxisAlignment.CENTER),
                padding=40,
                bgcolor=ft.Colors.PINK_700,
                alignment=ft.alignment.center,
                border_radius=ft.border_radius.only(bottom_left=25, bottom_right=25)
            ),
            ft.Column([
                self._create_profile_info_card("Email", ft.Icons.EMAIL, user_info.get('email', 'No disponible')),
                ft.Container(
                    content=ft.Column([
                        self._create_profile_option("Pedidos", ft.Icons.HISTORY),
                        self._create_profile_option("Favoritos", ft.Icons.FAVORITE),
                        self._create_profile_option("Configuraci\u00f3n", ft.Icons.SETTINGS)
                    ]),
                    margin=20
                ),
                ft.ElevatedButton(
                    "Cerrar Sesi\u00f3n",
                    icon=ft.Icons.LOGOUT,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.RED,
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=25),
                        padding=15
                    ),
                    on_click=lambda e: self.controller.logout()
                )
            ])
        ], scroll=ft.ScrollMode.AUTO)

    def _create_profile_info_card(self, title, icon, value):
        return ft.Card(
            content=ft.Container(
                content=ft.Row([
                    ft.Icon(icon, color=ft.Colors.PINK_700),
                    ft.Column([
                        ft.Text(title, size=14, color=ft.Colors.GREY),
                        ft.Text(value, size=16, weight=ft.FontWeight.W_500)
                    ], spacing=2)
                ], spacing=15),
                padding=20
            ),
            margin=ft.margin.symmetric(horizontal=20, vertical=10),
            elevation=2
        )

    def _create_profile_option(self, text, icon):
        return ft.ListTile(
            leading=ft.Icon(icon, color=ft.Colors.PINK_700),
            title=ft.Text(text, size=16),
            trailing=ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=16, color=ft.Colors.GREY),
            on_click=lambda e: print(f"Selected: {text}")
        )
