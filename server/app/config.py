# server/app/config.py

import os
from dotenv import load_dotenv
import secrets

# Load environment variables from .env file
load_dotenv()

class Settings:
    # Cryptographic Parameters
    ZKP_PRIME = int(os.getenv("ZKP_PRIME"), 16)
    ZKP_GENERATOR = int(os.getenv("ZKP_GENERATOR"))
    
    # Generate server's key pair
    ZKP_SECRET = secrets.randbelow(ZKP_PRIME - 1) + 1  # Securely generate secret
    ZKP_PUBLIC_KEY = pow(ZKP_GENERATOR, ZKP_SECRET, ZKP_PRIME)

    # File Paths
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")

    # Server Configuration
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 8000))

settings = Settings()

