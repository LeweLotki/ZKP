# client/client/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # Server Configuration
    SERVER_URL = os.getenv("SERVER_URL", "http://127.0.0.1:8000")
    
    # Cryptographic Parameters
    ZKP_PRIME = int(os.getenv("ZKP_PRIME"), 16)
    ZKP_GENERATOR = int(os.getenv("ZKP_GENERATOR"))

settings = Settings()

