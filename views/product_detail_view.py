import flet as ft
from controllers.product_detail_controller import ProductDetailController
import time

class ProductDetailView:
    def __init__(self, page: ft.Page, product_id: int):
        self.page = page
        self.product_id = product_id
        self.controller = ProductDetailController(self, product_id)
        
        self.images = []
        self.current_image_index = 0
        
        self.quantity_text = ft.Text(str(self.controller.selected_quantity), size=20, weight="bold")
        self.add_to_cart_button = ft.ElevatedButton(
            "🛒 Agregar al Carrito", icon=ft.Icons.ADD_SHOPPING_CART, height=60, expand=True,
            on_click=self.controller.add_to_cart,
            style=ft.ButtonStyle(
                bgcolor="#6A0DAD", color="#FFFFFF", elevation=4,
                shape=ft.RoundedRectangleBorder(radius=15),
                text_style=ft.TextStyle(size=16, weight="bold")
            )
        )
        self.image_container = ft.Container(
            alignment=ft.alignment.center,
            animate_opacity=200
        )
        self.indicators_container = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=12)
        
        self.build()

    def build(self):
        self.page.controls.clear()
        self.page.appbar = ft.AppBar(
            title=ft.Text("Detalles del Producto", size=22, weight="bold"),
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK, on_click=lambda _: self.page.go("/menu"),
                icon_color=ft.Colors.WHITE
            ),
            bgcolor=ft.Colors.PURPLE, elevation=0
        )
        self.page.scroll = ft.ScrollMode.ADAPTIVE
        self.page.bgcolor = ft.Colors.GREY_50
        
        self.layout = ft.Column(
            [ft.ProgressRing(color=ft.Colors.PURPLE)],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
            expand=True
        )
        
        self.page.add(self.layout)
        self.page.update()
        self.controller.main()

    def update_image_display(self):
        if not self.images:
            self.image_container.content = ft.Icon(ft.Icons.IMAGE_NOT_SUPPORTED, size=100, color=ft.Colors.GREY)
            self.page.update()
            return

        self.image_container.opacity = 0
        self.page.update()
        time.sleep(0.2)

        self.image_container.content = ft.Image(
            src=self.images[self.current_image_index],
            fit=ft.ImageFit.CONTAIN,
            error_content=ft.Icon(ft.Icons.BROKEN_IMAGE, size=60)
        )
        
        self.indicators_container.controls.clear()
        for i, _ in enumerate(self.images):
            self.indicators_container.controls.append(
                ft.Container(
                    width=25 if i == self.current_image_index else 10,
                    height=10,
                    bgcolor=ft.Colors.PURPLE if i == self.current_image_index else ft.Colors.GREY_400,
                    border_radius=5,
                    animate=ft.Animation(300, "ease"),
                    on_click=lambda e, index=i: self.goto_image(index)
                )
            )

        self.image_container.opacity = 1
        self.page.update()

    def previous_image(self, e):
        if self.images:
            self.current_image_index = (self.current_image_index - 1) % len(self.images)
            self.update_image_display()

    def next_image(self, e):
        if self.images:
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            self.update_image_display()

    def goto_image(self, index):
        if 0 <= index < len(self.images):
            self.current_image_index = index
            self.update_image_display()
            
    def display_product(self, product):
        self.images = product.get('imagenes_urls', [])
        stock = product.get('stock', 0)
        is_available = stock > 0

        nav_buttons = ft.Row(
            [
                ft.IconButton(icon=ft.Icons.ARROW_BACK_IOS_NEW, on_click=self.previous_image),
                ft.Container(expand=True),
                ft.IconButton(icon=ft.Icons.ARROW_FORWARD_IOS, on_click=self.next_image),
            ],
            visible=len(self.images) > 1
        )
        
        actions_panel = ft.Card(
            elevation=4, margin=ft.margin.symmetric(horizontal=16, vertical=8),
            shape=ft.RoundedRectangleBorder(radius=16),
            content=ft.Container(
                padding=ft.padding.all(20),
                content=ft.Column([
                    ft.Row([
                        ft.Text("Cantidad:", size=18, weight="bold", expand=True),
                        ft.IconButton(icon=ft.Icons.REMOVE, on_click=self.controller.decrement_quantity, disabled=not is_available),
                        self.quantity_text,
                        ft.IconButton(icon=ft.Icons.ADD, on_click=self.controller.increment_quantity, disabled=not is_available),
                    ]),
                    ft.Container(height=10),
                    self.add_to_cart_button
                ], spacing=10)
            )
        )

        self.layout.controls.clear()
        self.layout.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
        self.layout.alignment = ft.MainAxisAlignment.START
        self.layout.spacing = 15

        self.layout.controls.extend([
            ft.Text(product.get('nombre', 'N/A'), size=28, weight="bold", text_align="center"),
            ft.Text(f"${product.get('precio', 0.0):.2f}", size=24, weight="bold", color="#6A0DAD", text_align="center"),
            
            ft.Container(
                content=ft.Column([
                    self.image_container,
                    nav_buttons,
                    self.indicators_container,
                ]),
                padding=10, border_radius=12, bgcolor=ft.Colors.WHITE,
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12)
            ),
            
            ft.Card(
                elevation=4, margin=ft.margin.symmetric(horizontal=16, vertical=8),
                shape=ft.RoundedRectangleBorder(radius=16),
                content=ft.Container(
                    padding=20,
                    content=ft.Text(product.get('descripcion', 'Sin descripción.'), size=16, text_align="justify")
                )
            ),
            actions_panel,
            ft.Container(height=20)
        ])
        
        self.update_image_display()

    def display_error(self, message):
        self.layout.controls.clear()
        self.layout.controls.append(ft.Text(message, size=18, text_align="center"))
        self.page.update()