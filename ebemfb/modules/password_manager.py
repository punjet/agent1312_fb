from cryptography.fernet import Fernet
from modules.config_loader import settings

cipher = Fernet(settings.password_manager_key)

def encrypt_password(password: str) -> str:
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(token: str) -> str:
    return cipher.decrypt(token.encode()).decode()