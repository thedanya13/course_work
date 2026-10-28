import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Сессионный токен на 5 минут
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=5)
    SESSION_COOKIE_HTTPONLY = True      
    SESSION_COOKIE_SECURE = False       
    SESSION_COOKIE_SAMESITE = 'Lax'     