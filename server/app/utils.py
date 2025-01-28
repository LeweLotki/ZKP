import os
import hashlib
from fastapi import UploadFile

def save_file(file: UploadFile, unique_id: str) -> str:
    """
    Save uploaded file to the uploads directory.
    """
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"{unique_id}.csv")
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return file_path

def calculate_checksum(file_path: str) -> str:
    """
    Calculate the SHA-256 checksum of a file.
    """
    with open(file_path, "rb") as f:
        content = f.read()
    return hashlib.sha256(content).hexdigest()

