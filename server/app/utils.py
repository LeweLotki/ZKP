# server/app/utils.py

import hashlib

def calculate_checksum(file_path: str) -> str:
    """Calculate the SHA-256 checksum of the given file."""
    with open(file_path, "rb") as f:
        file_content = f.read()
        return hashlib.sha256(file_content).hexdigest()

