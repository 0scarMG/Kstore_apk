# views/menu_view.py
import flet as ft
from controllers.menu_controller import MenuController
from components.store_components import Navbar, StoreLayout, BottomNavBar

class MenuView:
    def __init__(self, page: ft.Page, go_to_route, user_data=None):
        """
        Inicializa la vista del menú principal (la tienda).
        """
        self.page = page
        self.go_to_route = go_to_route
        self.user_data = user_data

        # 1. Instanciar el controlador PRIMERO y asignarlo a self.controller
        # Esto crea el atributo 'controller' en el objeto 'MenuView'.
        self.controller = MenuController()

        # 2. AHORA que self.controller existe, puedes usarlo para inicializar otros componentes.
        self.store_layout = StoreLayout(self.controller, self.page)
        self.navbar = Navbar(self.controller)
        
        # 3. AGREGAR LA BARRA DE NAVEGACIÓN INFERIOR
        self.bottom_nav = BottomNavBar(self.go_to_route)

        # 4. Construir la UI de esta vista
        self.build()

    def build(self):
        """Configura la página con los componentes de la tienda."""
        # Asignar la barra de navegación superior a la página
        self.page.appbar = self.navbar
        
        # AGREGAR LA BARRA DE NAVEGACIÓN INFERIOR
        self.page.navigation_bar = self.bottom_nav
        
        # Limpiar contenido previo de la página
        self.page.controls.clear()
        
        # Añadir el layout principal de la tienda (grid, preloader, etc.)
        self.page.add(self.store_layout.build())
        
        # CREAR Y MOSTRAR el mensaje de bienvenida CORRECTAMENTE
        if self.user_data:
            welcome_name = self.user_data.get('usuario', 'Usuario')
            # Crear el SnackBar correctamente
            welcome_snack = ft.SnackBar(
                content=ft.Text(f"¡Bienvenido de vuelta, {welcome_name}!"),
                duration=3000,  # Mostrar por 3 segundos
                bgcolor=ft.Colors.PURPLE_700,
                action="OK"
            )
            # IMPORTANTE: Agregar el SnackBar a la página ANTES de abrirlo
            self.page.overlay.append(welcome_snack)
            welcome_snack.open = True
        
        # Actualizar la página antes de iniciar el controlador
        self.page.update()
        
        # Iniciar la lógica del controlador para cargar datos
        self.controller.main()