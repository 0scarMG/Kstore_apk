import flet as ft

PURPLE = "#6A0DAD"
WHITE = "#FFFFFF"

class Navbar(ft.AppBar):
    def __init__(self, controller, on_filter_click):
        super().__init__()
        self.controller = controller
        
        self.search_bar = ft.TextField(
            hint_text="Buscar en Kstore...", expand=True, bgcolor=ft.Colors.WHITE,
            color=ft.Colors.BLACK, border_radius=8, border_color=ft.Colors.GREY_300,
            height=45, content_padding=ft.padding.only(left=15, top=5),
            hint_style=ft.TextStyle(color=ft.Colors.GREY_500),
            on_change=self.on_search_change, prefix_icon=ft.Icons.SEARCH
        )
        self.title = self.search_bar
        self.bgcolor = ft.Colors.WHITE
        self.elevation = 2

        self.actions = [
            ft.IconButton(
                icon=ft.Icons.FILTER_LIST_ROUNDED, icon_color=ft.Colors.GREY_700,
                on_click=on_filter_click, tooltip="Filtrar productos"
            ),
        ]

    def on_search_change(self, e):
        self.controller.search_products(e.control.value)

class BottomNavBar(ft.NavigationBar):
    def __init__(self, go_to_route):
        super().__init__()
        self.go_to_route = go_to_route
        self.bgcolor = ft.Colors.WHITE
        self.surface_tint_color = PURPLE
        self.indicator_color = ft.Colors.PURPLE_50
        self.selected_index = 0
        self.on_change = self.handle_nav_change
        
        self.destinations = [
            ft.NavigationBarDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Inicio"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON_OUTLINE, selected_icon=ft.Icons.PERSON, label="Cuenta"),
            ft.NavigationBarDestination(icon=ft.Icons.SHOPPING_CART_OUTLINED, selected_icon=ft.Icons.SHOPPING_CART, label="Carrito"),
            ft.NavigationBarDestination(icon=ft.Icons.MENU_OUTLINED, selected_icon=ft.Icons.MENU, label="Menú"),
        ]

    def handle_nav_change(self, e):
        selected_label = self.destinations[e.control.selected_index].label
        print(f"Navegando a: {selected_label}")

class ProductCard(ft.Card):
    def __init__(self, controller, product_data):
        super().__init__(width=280, height=380)
        self.controller = controller
        self.product_data = product_data
        
        self.content = ft.Container(
            content=ft.Column([
                ft.Image(
                    src=product_data.get('imagenes_urls', [None])[0] or 'https://placehold.co/280x200/6A0DAD/FFFFFF?text=K-POP',
                    height=200, width=280, fit=ft.ImageFit.COVER,
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
                                    "Agregar", icon=ft.Icons.ADD_SHOPPING_CART,
                                    bgcolor=PURPLE, color=WHITE,
                                    on_click=self.add_to_cart_click
                                )
                            ]
                        )
                    ])
                )
            ]),
            on_click=self.view_details_click
        )

    def add_to_cart_click(self, e: ft.ControlEvent):
        e.stop_propagation = True 
        self.controller.add_to_cart(self.product_data)
        
    def view_details_click(self, e: ft.ControlEvent):
        self.controller.view_product_details(self.product_data)

class FilterBottomSheet(ft.BottomSheet):
    def __init__(self, controller, categories, max_price):
        self.controller = controller
        self.category_dropdown = ft.Dropdown(
            hint_text="Todas las categorías",
            options=[ft.dropdown.Option(cat) for cat in categories],
            border_radius=ft.border_radius.all(8),
        )
        self.price_slider = ft.RangeSlider(
            min=0, max=max_price, start_value=0, end_value=max_price,
            divisions=20, label="{value} $",
        )
        self.sort_radio_group = ft.RadioGroup(content=ft.Column([
            ft.Radio(value="popularity", label="Más populares"),
            ft.Radio(value="price_asc", label="Precio: de menor a mayor"),
            ft.Radio(value="price_desc", label="Precio: de mayor a menor"),
        ]), value="popularity")

        main_content = ft.Container(
            padding=ft.padding.only(left=20, right=20, top=10, bottom=30),
            content=ft.ListView(
                controls=[
                    ft.Row([
                        ft.Text("Filtros y Orden", size=18, weight="bold", expand=True),
                        ft.IconButton(icon=ft.Icons.CLOSE, on_click=self.close_sheet)
                    ]),
                    ft.Divider(), ft.Text("Categoría", weight="bold"), self.category_dropdown,
                    ft.Divider(height=10), ft.Text("Rango de Precio", weight="bold"), self.price_slider,
                    ft.Divider(height=10), ft.Text("Ordenar por", weight="bold"), self.sort_radio_group,
                    ft.Divider(height=20),
                    ft.ElevatedButton(
                        "APLICAR FILTROS", on_click=self.apply_filters_click, expand=True, height=50,
                        style=ft.ButtonStyle(bgcolor=PURPLE, color=WHITE)
                    ),
                    ft.TextButton(
                        "Limpiar Filtros", on_click=self.clear_filters_click, expand=True
                    )
                ], spacing=10,
            )
        )
        super().__init__(content=main_content, open=False)

    def apply_filters_click(self, e):
        filters = {
            "category": self.category_dropdown.value,
            "price_range": (self.price_slider.start_value, self.price_slider.end_value),
            "sort_by": self.sort_radio_group.value
        }
        self.controller.apply_filters(filters)
        self.close_sheet(e)

    def clear_filters_click(self, e):
        self.category_dropdown.value = None
        self.price_slider.start_value = 0
        if self.price_slider.max is not None:
            self.price_slider.end_value = self.price_slider.max
        self.sort_radio_group.value = "popularity"
        self.controller.apply_filters({})
        self.close_sheet(e)

    def close_sheet(self, e):
        self.open = False
        self.update()

class StoreLayout:
    def __init__(self, controller, page: ft.Page):
        self.controller = controller
        self.page = page
        self.controller.view = self

        self.preloader = ft.Column(
            [ft.ProgressRing(), ft.Text("Cargando productos...")],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER, expand=True, visible=False
        )
        self.products_grid = ft.ResponsiveRow(
            controls=[], alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.START,
            run_spacing=20, spacing=20
        )
        self.grid_container = ft.Container(
            padding=20, content=self.products_grid, visible=False
        )
        self.container = ft.Stack(
            controls=[self.grid_container, self.preloader], expand=True
        )

    def build(self):
        return self.container

    def update_view(self, products: list):
        self.products_grid.controls.clear()
        if not products:
            self.products_grid.controls.append(
                ft.Text("No se encontraron productos.", size=18, text_align="center", width=self.page.width)
            )
        else:
            for product in products:
                card = ProductCard(self.controller, product)
                self.products_grid.controls.append(
                    ft.Column([card], col={"xs": 12, "sm": 6, "md": 4, "xl": 3})
                )
        self.grid_container.visible = True
        self.preloader.visible = False
        self.page.update()

    def show_preloader(self, show: bool):
        self.preloader.visible = show
        self.grid_container.visible = not show
        self.page.update()

    def show_db_error(self):
        self.preloader.visible = False
        self.grid_container.visible = False
        error_snack = ft.SnackBar(
            content=ft.Row([
                ft.Icon(ft.Icons.ERROR_OUTLINE, color=WHITE),
                ft.Text("Error: No se pudo conectar a la base de datos.")
            ], alignment="center"),
            duration=5000, bgcolor=ft.Colors.RED_400, action="REINTENTAR"
        )
        if self.page and self.page.overlay is not None:
            self.page.overlay.append(error_snack)
            error_snack.open = True
            self.page.update()