import re

def validate_email_format(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def validate_password_strength(password: str) -> str:
    if len(password) < 6:
        return "La contraseña debe tener al menos 6 caracteres"
    elif len(password) < 8:
        return "Contraseña débil. Se recomienda al menos 8 caracteres"
    return ""  # válida
