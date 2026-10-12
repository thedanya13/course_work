import os
from cryptography.fernet import Fernet


ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')
if not ENCRYPTION_KEY:
    ENCRYPTION_KEY = Fernet.generate_key().decode()
    print(f"⚠️ Сгенерирован ключ! Добавь в .env строку: ENCRYPTION_KEY={ENCRYPTION_KEY}")

fernet = Fernet(ENCRYPTION_KEY.encode())

def encrypt_data(data: str) -> str:
    if data:
        return fernet.encrypt(data.encode()).decode()
    return None

def decrypt_data(data: str) -> str:
    if data:
        return fernet.decrypt(data.encode()).decode()
    return None