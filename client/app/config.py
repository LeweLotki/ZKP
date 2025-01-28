from decouple import config

class Settings:
    ZKP_PRIME = int(config("ZKP_PRIME"), 16)
    ZKP_GENERATOR = config("ZKP_GENERATOR", cast=int)
    SERVER_URL = config("SERVER_URL", default="http://127.0.0.1:8000")

settings = Settings()

