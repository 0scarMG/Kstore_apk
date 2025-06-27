import flet as ft
from models.user_model import UserModel

class RegisterView:
    def __init__(self, page: ft.Page, go_to_route):
        self.page = page
        self.go_to_route = go_to_route
        self.page.title = "Register MVC"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.on_resized = lambda e: self.page.update()
        self.page.bgcolor = "#f0f2f5"

        self.NameUSer = ft.TextField(
            label="Nombre",
            text_style=ft.TextStyle(color="#333333"),
            border=ft.InputBorder.OUTLINE,
            border_radius=10,
            border_color=ft.Colors.GREY_400,
            focused_border_color="#bd1ee5",
            content_padding=15,
            text_size=14,
            bgcolor=ft.Colors.WHITE70  # Fondo semi-transparente
        )
        
        self.EmailUser = ft.TextField(
            label="Correo",
            text_style=ft.TextStyle(color="#333333"),
            border=ft.InputBorder.OUTLINE,
            border_radius=10,
            border_color=ft.Colors.GREY_400,
            focused_border_color="#bd1ee5",
            content_padding=15,
            text_size=14,
            on_change=self.on_email_change,
            bgcolor=ft.Colors.WHITE70  # Fondo semi-transparente
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
            on_change=self.on_password_change,
            bgcolor=ft.Colors.WHITE70  # Fondo semi-transparente
        )

        self.ConfirmPassword = ft.TextField(
            label="Confirmación de contraseña",
            text_style=ft.TextStyle(color="#333333"),
            password=True,
            can_reveal_password=True,
            border=ft.InputBorder.OUTLINE,
            border_radius=10,
            border_color=ft.Colors.GREY_400,
            focused_border_color="#bd1ee5",
            content_padding=15,
            text_size=14,
            bgcolor=ft.Colors.WHITE70  # Fondo semi-transparente
        )

        self.message = ft.Text(color=ft.Colors.RED, size=12)

        self.register_button = ft.ElevatedButton(
            text="Registrarse",
            on_click=self.on_register,
            bgcolor="#bd1ee5",
            color="white",
            width=400,
            height=45,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
        )

        # Inicializar el controlador
        self.controller = UserModel(self)

        # Construcción del formulario con imagen de fondo correcta
        register_form = ft.Container(
            content=ft.Stack(
                controls=[
                    # Imagen de fondo - debe ir PRIMERO en el Stack
                    ft.Container(
                        content=ft.Image(
                            src="../img/register.png",
                            fit=ft.ImageFit.COVER,
                            opacity=0.5  # Más transparente para mejor legibilidad
                        ),
                        width=700,
                        height=900,
                        border_radius=15,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE
                    ),
                    
                    # Contenido del formulario - va ENCIMA de la imagen
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                # Título
                                ft.Container(
                                    content=ft.Text(
                                        "Registro de usuarios",
                                        size=28,
                                        weight=ft.FontWeight.BOLD,
                                        color="#2c3e50",
                                        text_align=ft.TextAlign.CENTER
                                    ),
                                    alignment=ft.alignment.center,
                                    padding=ft.padding.only(top=30, bottom=20),
                                    width=400
                                ),
                                
                                # Campos del formulario
                                self.NameUSer,
                                ft.Container(height=15),
                                self.EmailUser,
                                ft.Container(height=15),
                                self.password,
                                ft.Container(height=15),
                                self.ConfirmPassword,
                                ft.Container(height=25),
                                
                                # Botón de registro
                                self.register_button,
                                
                                # Separador
                                ft.Container(height=20),
                                ft.Divider(color=ft.Colors.GREY_400, thickness=1),
                                ft.Container(height=10),
                                
                                # Texto "O regístrese con"
                                ft.Text(
                                    "O regístrese con",
                                    size=14,
                                    color=ft.Colors.BLUE_GREY_600,
                                    text_align=ft.TextAlign.CENTER,
                                    weight=ft.FontWeight.W_500
                                ),
                                
                                ft.Container(height=15),
                                
                                # Botón de Google
                                ft.Row(
                                    controls=[
                                        ft.Container(
                                            content=ft.Image(
                                                src="../img/google.png",
                                                width=30,
                                                height=30,
                                                fit=ft.ImageFit.CONTAIN
                                            ),
                                            width=50,
                                            height=50,
                                            border_radius=25,
                                            bgcolor=ft.Colors.WHITE,
                                            border=ft.border.all(2, ft.Colors.GREY_300),
                                            alignment=ft.alignment.center,
                                            on_click=lambda e: self.show_message("Google login no implementado aún"),
                                            shadow=ft.BoxShadow(
                                                blur_radius=8, 
                                                color=ft.Colors.GREY_400,
                                                offset=ft.Offset(0, 2)
                                            )
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=15,
                                ),
                                
                                ft.Container(height=20)  # Espaciado inferior
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0,
                            scroll=ft.ScrollMode.AUTO  # Permitir scroll si es necesario
                        ),
                        width=500,
                        height=600,
                        padding=ft.padding.symmetric(horizontal=50, vertical=20),
                        alignment=ft.alignment.center
                    )
                ],
                width=500,
                height=600
            ),
            width=500,
            height=600,
            border_radius=15,
            border=ft.border.all(1, ft.Colors.GREY_300),
            shadow=ft.BoxShadow(
                blur_radius=25, 
                color=ft.Colors.GREY_400,
                offset=ft.Offset(0, 8)
            ),
            bgcolor=ft.Colors.WHITE,
            clip_behavior=ft.ClipBehavior.HARD_EDGE
        )
        
        # Agregar todo a la página
        self.page.add(
            ft.Column(
                controls=[
                    register_form, 
                    ft.Container(height=10),
                    self.message,
                    ft.TextButton(
                        "¿Ya tienes una cuenta? Inicia sesión",
                        on_click=lambda e: self.go_to_route("/login")
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            )
        )

    def on_register(self, e):
        self.controller.register(
            self.NameUSer.value,
            self.EmailUser.value,
            self.password.value,
            self.ConfirmPassword.value
        )

    def on_email_change(self, e):
        if e.control.value:
            self.controller.validate_email_format(e.control.value)

    def on_password_change(self, e):
        self.controller.check_password_strength(e.control.value)

    def show_message(self, text):
        self.message.value = text
        self.message.color = ft.Colors.RED
        self.page.update()

    def show_success_message(self, text):
        self.message.value = text
        self.message.color = ft.Colors.GREEN
        self.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("¡Éxito!"),
            content=ft.Text(text),
            actions=[
                ft.TextButton("OK", on_click=lambda e: self.close_dialog())
            ]
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def close_dialog(self):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()