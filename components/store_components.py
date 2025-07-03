# components/store_components.py
import flet as ft

PURPLE = "#6A0DAD"
WHITE = "#FFFFFF"

# --- Barra Superior (Estilo Amazon) ---
# CORRECCIÓN: Se revierte el nombre de 'TopBar' a 'Navbar' para que coincida con la importación.
class Navbar(ft.AppBar):
    """La barra de navegación superior, ahora enfocada en la búsqueda."""
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        self.search_bar = ft.TextField(
            hint_text="Buscar en Kstore...",
            expand=True,
            bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK,
            border_radius=8,
            border_color=ft.Colors.GREY_300,
            height=45,
            content_padding=ft.padding.only(left=15, top=5),
            hint_style=ft.TextStyle(color=ft.Colors.GREY_500),
            on_change=self.on_search_change,
            prefix_icon=ft.Icons.SEARCH
        )
        
        # La AppBar ahora es más simple
        self.title = self.search_bar
        self.bgcolor = ft.Colors.WHITE
        self.elevation = 2 # Sombra sutil
        self.actions = [
            ft.IconButton(
                icon=ft.Icons.CAMERA_ALT_OUTLINED, 
                icon_color=ft.Colors.GREY_700,
                tooltip="Búsqueda por imagen"
            ),
        ]

    def on_search_change(self, e):
        self.controller.search_products(e.control.value)

# --- Barra de Navegación Inferior ---
class BottomNavBar(ft.NavigationBar):
    """La nueva barra de navegación en la parte inferior de la pantalla."""
    def __init__(self, go_to_route):
        super().__init__()
        self.go_to_route = go_to_route
        self.bgcolor = ft.Colors.WHITE
        self.surface_tint_color = PURPLE
        self.indicator_color = ft.Colors.PURPLE_50
        self.selected_index = 0 # Inicia en 'Inicio'
        self.on_change = self.handle_nav_change
        
        self.destinations = [
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Inicio"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, selected_icon=ft.Icons.PERSON, label="Cuenta"),
            ft.NavigationBarDestination(icon=ft.Icons.SHOPPING_CART_OUTLINED, selected_icon=ft.Icons.SHOPPING_CART, label="Carrito"),
            ft.NavigationBarDestination(icon=ft.Icons.MENU_OUTLINED, selected_icon=ft.Icons.MENU, label="Menú"),
        ]

    def handle_nav_change(self, e):
        """Maneja los clics en los iconos de navegación."""
        selected_label = self.destinations[e.control.selected_index].label
        print(f"Navegando a: {selected_label}")
        # Aquí puedes agregar la lógica para cambiar de vista con self.go_to_route
        # Ejemplo:
        # if selected_label == "Cuenta":
        #     self.go_to_route("/profile")
        # elif selected_label == "Inicio":
        #     self.go_to_route("/menu")


# --- Componentes de Productos (sin cambios) ---
class ProductCard(ft.Card):
    """Tarjeta individual para mostrar un producto."""
    def __init__(self, controller, product_data):
        super().__init__(width=280, height=380)
        self.controller = controller
        self.product_data = product_data

        self.content = ft.Column([
            ft.Image(
                src=product_data.get('imagen_url', 'https://placehold.co/280x200/6A0DAD/FFFFFF?text=K-POP'),
                height=200,
                width=280,
                fit=ft.ImageFit.COVER,
                border_radius=ft.border_radius.only(top_left=10, top_right=10),
                error_content=ft.Icon(ft.Icons.BROKEN_IMAGE, size=50)
            ),
            ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text(product_data.get('nombre', 'N/A'), weight="bold", size=16),
                    ft.Text(f"Categoría: {product_data.get('categoria', 'N/A')}", size=12, color=ft.Colors.GREY),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(f"${product_data.get('precio', 0.0):.2f}", size=20, weight="bold", color=PURPLE),
                            ft.ElevatedButton(
                                "Agregar",
                                icon=ft.Icons.ADD_SHOPPING_CART,
                                bgcolor=PURPLE,
                                color=WHITE,
                                on_click=self.add_to_cart_click
                            )
                        ]
                    )
                ])
            )
        ])

    def add_to_cart_click(self, e):
        self.controller.add_to_cart(self.product_data)

class StoreLayout:
    def __init__(self, controller, page: ft.Page):
        self.controller = controller
        self.page = page
        self.controller.view = self

        # 1. El preloader de columna, que ahora será el protagonista.
        self.preloader = ft.Column(
            [ft.ProgressRing(), ft.Text("Cargando productos...")],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
            visible=False  # Inicialmente oculto
        )

        self.products_grid = ft.ResponsiveRow(
            controls=[],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.START,
            run_spacing=20,
            spacing=20
        )
        
        # Contenedor para la parrilla de productos, también controlaremos su visibilidad
        self.grid_container = ft.Container(
            padding=20,
            content=self.products_grid,
            expand=True,
            visible=False # Inicialmente oculto
        )

        # 2. El layout principal ahora es un Stack.
        # Un Stack permite apilar widgets uno encima del otro.
        # Pondremos la parrilla de productos y el preloader en el mismo lugar.
        self.container = ft.Stack(
            controls=[
                self.grid_container,
                self.preloader,
            ],
            expand=True
        )

    def build(self):
        # El método build ahora devuelve el Stack
        return self.container

    def update_view(self, products: list):
        self.products_grid.controls.clear()
        if not products:
            self.products_grid.controls.append(
                ft.Text("No se encontraron productos.", size=18, text_align="center", width=self.page.width)
            )
        else:
            for product in products:
                # Asumo que ProductCard está definido en este mismo archivo
                card = ProductCard(self.controller, product)
                self.products_grid.controls.append(
                    ft.Column([card], col={"xs": 12, "sm": 6, "md": 4, "xl": 3})
                )
        
        # Al actualizar la vista, hacemos visible la parrilla y ocultamos el preloader
        self.grid_container.visible = True
        self.preloader.visible = False
        self.page.update()

    def show_preloader(self, show: bool):
        # 3. Este método ahora es mucho más simple y robusto.
        # Simplemente alterna la visibilidad de los dos componentes principales.
        self.preloader.visible = show
        self.grid_container.visible = not show
        self.page.update()

    def show_db_error(self):
        # Ocultamos todo en la vista principal
        self.preloader.visible = False
        self.grid_container.visible = False
        
        # Mostramos el error en un SnackBar (esto está bien para errores)
        error_snack = ft.SnackBar(
            content=ft.Row([
                ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.WHITE),
                ft.Text("Error: No se pudo conectar a la base de datos.")
            ], alignment="center"),
            duration=5000,
            bgcolor=ft.Colors.RED_400,
            action="REINTENTAR"
        )
        self.page.overlay.append(error_snack)
        error_snack.open = True
        self.page.update()