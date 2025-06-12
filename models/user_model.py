from config.db import db_instance
from pymongo.errors import DuplicateKeyError
import bcrypt
import re
from datetime import datetime

class UserModel:
    def __init__(self):
        try:
            self.collection = db_instance.get_collection("usuario")
            self.collection.create_index("email", unique=True)
        except Exception as e:
            print(f"Error al conectar con MongoDB: {e}")
            self.collection = None

    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validate_password(self, password):
        return len(password) >= 6

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed)

    def email_exists(self, email):
        if self.collection is None:
            return False
        return self.collection.find_one({"email": email}) is not None

    def create_user(self, name, email, password):
        try:
            if self.collection is None:
                return {"success": False, "message": "Error de conexión a la base de datos"}

            if not name or not name.strip():
                return {"success": False, "message": "El nombre es requerido"}

            if not self.validate_email(email):
                return {"success": False, "message": "Formato de email inválido"}

            if not self.validate_password(password):
                return {"success": False, "message": "La contraseña debe tener al menos 6 caracteres"}

            if self.email_exists(email):
                return {"success": False, "message": "El email ya está registrado"}

            user_data = {
                "usuario": name.strip(),
                "email": email.lower().strip(),
                "password": self.hash_password(password),
                "created_at": datetime.now(),
                "is_active": True
            }

            result = self.collection.insert_one(user_data)
            return {"success": True, "message": "Usuario registrado exitosamente"} if result.inserted_id else {"success": False, "message": "Error al registrar el usuario"}

        except DuplicateKeyError:
            return {"success": False, "message": "El email ya está registrado"}
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            return {"success": False, "message": "Error interno del servidor"}

    def validate_user(self, email, password):
        """Valida las credenciales de un usuario"""
        if self.collection is None:
            return False

        user = self.collection.find_one({"email": email.lower().strip()})
        if not user:
            return False

        return self.check_password(password, user["password"])

    def get_user_by_email(self, email):
        if self.collection is None:
            return None
        return self.collection.find_one({"email": email.lower().strip()})

    def close_connection(self):
        db_instance.close()
