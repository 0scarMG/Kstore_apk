import flet as ft
from controllers.user_controller import UserController

class LoginView:
    def __init__(self, page: ft.Page, go_to_route):
        self.page = page
        self.go_to_route = go_to_route
        self.page.title = "Login MVC"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.on_resized = lambda e: self.page.update()
        self.page.bgcolor = "#f0f2f5"

        # Controles principales
        self.username = ft.TextField(
            label="Correo Electrónico",
            text_style=ft.TextStyle(color="#333333"),
            border=ft.InputBorder.OUTLINE,
            border_radius=10,
            border_color=ft.Colors.GREY_400,
            focused_border_color="#bd1ee5",
            content_padding=15,
            text_size=14,
            bgcolor=ft.Colors.WHITE70  # Agregado como en RegisterView
        )

        self.password = ft.TextField(
            label="Contraseña",
            text_style=ft.TextStyle(color="#333333"),
            password=True,
            can_reveal_password=True,
            border=ft.InputBorder.OUTLINE,
            border_radius=10,
            border_color=ft.Colors.GREY_400,
            focused_border_color="#bd1ee5",
            content_padding=15,
            text_size=14,
            bgcolor=ft.Colors.WHITE70  # Agregado como en RegisterView
        )

        self.message = ft.Text(color="red")

        self.login_button = ft.ElevatedButton(
            text="Iniciar Sesión",
            on_click=self.on_login,
            bgcolor="#bd1ee5",
            color="white",
            width=400,
            height=45,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
        )

        self.forgot_password = ft.TextButton(
            text="¿Olvidaste tu contraseña?",
            style=ft.ButtonStyle(color="#1e3ce5")
        )

        self.controller = UserController(self)

        # Construcción del formulario de login con las dimensiones del RegisterView
        login_form = ft.Container(
            content=ft.Stack(
                controls=[
                    # Imagen de fondo - DIMENSIONES DEL REGISTERVIEW
                    ft.Container(
                        content=ft.Image(
                            src="../img/register.png",
                            fit=ft.ImageFit.COVER,
                            opacity=0.5  # Aplicando la opacidad como en RegisterView
                        ),
                        width=700,  # Manteniendo las dimensiones del RegisterView
                        height=900, # Manteniendo las dimensiones del RegisterView
                        border_radius=15,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE
                    ),
                    
                    # Contenido del formulario - DIMENSIONES DEL REGISTERVIEW
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                # Título
                                ft.Container(
                                    content=ft.Text(
                                        "Iniciar Sesión",
                                        size=28,  # Tamaño del RegisterView
                                        weight=ft.FontWeight.BOLD,
                                        color="#2c3e50",  # Color del RegisterView
                                        text_align=ft.TextAlign.CENTER
                                    ),
                                    alignment=ft.alignment.center,
                                    padding=ft.padding.only(top=30, bottom=20),  # Padding del RegisterView
                                    width=400
                                ),
                                
                                # Campos del formulario con espaciado del RegisterView
                                self.username,
                                ft.Container(height=15),
                                ft.Column(
                                    controls=[
                                        self.password,
                                        ft.Container(height=15),
                                        ft.Container(
                                            content=self.forgot_password,
                                            alignment=ft.alignment.top_center,
                                        )
                                    ]
                                ),
                                ft.Container(height=25),  # Espaciado del RegisterView
                                self.login_button,
                                
                                # Separador como en RegisterView
                                ft.Container(height=20),
                                ft.Divider(color=ft.Colors.GREY_400, thickness=1),
                                ft.Container(height=10),
                                
                                ft.TextButton(
                                    text="¿No tienes cuenta? Regístrate aquí",
                                    style=ft.ButtonStyle(color="#1e3ce5"),
                                    on_click=lambda e: self.go_to_route("/register")
                                ),
                                
                                # Texto "O inicia sesión con" estilo RegisterView
                                ft.Text(
                                    "O inicia sesión con",
                                    size=14,
                                    color=ft.Colors.BLUE_GREY_600,  # Color del RegisterView
                                    text_align=ft.TextAlign.CENTER,
                                    weight=ft.FontWeight.W_500  # Peso del RegisterView
                                ),
                                
                                ft.Container(height=15),
                                
                                # Botón de Google con estilo del RegisterView
                                ft.Row(
                                    controls=[
                                        ft.Container(
                                            content=ft.Image(
                                                src="../img/google.png",
                                                width=30,  # Dimensiones del RegisterView
                                                height=30,
                                                fit=ft.ImageFit.CONTAIN
                                            ),
                                            width=50,
                                            height=50,
                                            border_radius=25,
                                            bgcolor=ft.Colors.WHITE,
                                            border=ft.border.all(2, ft.Colors.GREY_300),  # Border del RegisterView
                                            alignment=ft.alignment.center,
                                            on_click=lambda e: self.show_message("Google login not implemented yet"),
                                            shadow=ft.BoxShadow(
                                                blur_radius=8,  # Shadow del RegisterView
                                                color=ft.Colors.GREY_400,
                                                offset=ft.Offset(0, 2)
                                            )
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=15,
                                ),
                                
                                ft.Container(height=20)  # Espaciado inferior del RegisterView
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0,
                            scroll=ft.ScrollMode.AUTO  # Scroll del RegisterView
                        ),
                        width=500,   # DIMENSIONES DEL REGISTERVIEW
                        height=600,  # DIMENSIONES DEL REGISTERVIEW
                        padding=ft.padding.symmetric(horizontal=50, vertical=20),  # Padding del RegisterView
                        alignment=ft.alignment.center
                    )
                ],
                width=500,   # DIMENSIONES DEL REGISTERVIEW
                height=600   # DIMENSIONES DEL REGISTERVIEW
            ),
            width=500,       # DIMENSIONES DEL REGISTERVIEW
            height=600,      # DIMENSIONES DEL REGISTERVIEW
            border_radius=15,
            border=ft.border.all(1, ft.Colors.GREY_300),
            shadow=ft.BoxShadow(
                blur_radius=25,  # Shadow del RegisterView
                color=ft.Colors.GREY_400,
                offset=ft.Offset(0, 8)
            ),
            bgcolor=ft.Colors.WHITE,  # Background del RegisterView
            clip_behavior=ft.ClipBehavior.HARD_EDGE
        )

        # Agregar elementos a la página
        self.page.add(
            ft.Column(
                controls=[
                    login_form, 
                    ft.Container(height=10),  # Espaciado como en RegisterView
                    self.message
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            )
        )

    def on_login(self, e):
        self.controller.login(self.username.value, self.password.value)

    def show_message(self, text):
        self.message.value = text
        self.page.update()