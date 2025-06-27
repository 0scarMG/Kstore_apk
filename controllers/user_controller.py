from models.user_model import UserModel
import services.validation_service as vs


class UserController:
    def __init__(self, view):
        self.model = UserModel()
        self.view = view

    def login(self, username, password):
        user_data = self.model.validate_user(username, password)
        if user_data:
            self.view.show_message("Login exitoso ✅")
            # Redirigir a la vista del menú pasando los datos del usuario
            self.view.go_to_menu(user_data)
        else:
            self.view.show_message("Credenciales inválidas ❌")
            

    def register(self, name, email, password, confirm_password):
        """Procesa el registro de un nuevo usuario"""
        try:
            # Validaciones del lado del controlador
            if not name or not name.strip():
                self.view.show_message("Por favor ingrese su nombre")
                return
            
            if not email or not email.strip():
                self.view.show_message("Por favor ingrese su correo electrónico")
                return
            
            if not password:
                self.view.show_message("Por favor ingrese una contraseña")
                return
            
            if not confirm_password:
                self.view.show_message("Por favor confirme su contraseña")
                return
            
            if password != confirm_password:
                self.view.show_message("Las contraseñas no coinciden")
                return
            
            # Intentar crear el usuario usando el modelo
            result = self.model.create_user(name, email, password)
            
            if result["success"]:
                self.view.show_success_message(result["message"])
                self.clear_form()
            else:
                self.view.show_message(result["message"])
                
        except Exception as e:
            print(f"Error en el controlador: {e}")
            self.view.show_message("Error interno. Por favor intente nuevamente.")
    
    def clear_form(self):
        """Limpia los campos del formulario después de un registro exitoso"""
        self.view.NameUSer.value = ""
        self.view.EmailUser.value = ""
        self.view.password.value = ""
        self.view.ConfirmPassword.value = ""
        self.view.page.update()
    
    def validate_email_format(self, email):
        if email and not vs.validate_email_format(email):
            self.view.show_message("Formato de email inválido")
            return False
        return True
    
    def check_password_strength(self, password):
        message = vs.validate_password_strength(password)
        self.view.show_message(message)  
    
    def cleanup(self):
        """Limpia recursos cuando se cierra la aplicación"""
        if self.model:
            self.model.close_connection()