from decouple import config

class Settings:
    ZKP_PRIME = int(config("ZKP_PRIME"), 16)
    ZKP_GENERATOR = config("ZKP_GENERATOR", cast=int)
    UPLOAD_DIR = config("UPLOAD_DIR", default="uploads")
    HOST = config("HOST", default="127.0.0.1")
    PORT = config("PORT", cast=int, default=8000)
    DATABASE_URL = config("DATABASE_URL")
settings = Settings()

