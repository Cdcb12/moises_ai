from decouple import config
import secrets

class Config:
    SECRET_KEY = config('SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = secrets.token_hex()  # Genera una clave secreta aleatoria

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}