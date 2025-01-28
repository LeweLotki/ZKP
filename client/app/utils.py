import hashlib
import requests
from app.config import settings

def calculate_checksum(file_path: str) -> str:
    """Calculate the SHA-256 checksum of a file."""
    with open(file_path, "rb") as f:
        content = f.read()
    return hashlib.sha256(content).hexdigest()

def upload_file(file_path: str, public_key: int) -> str:
    """Upload a file to the server along with the public key."""
    with open(file_path, "rb") as f:
        response = requests.post(
            f"{settings.SERVER_URL}/upload-csv/",
            files={"file": f},
            data={"public_key": str(public_key)}
        )
    
    if response.status_code == 200:
        return response.json().get("id")
    print(f"Error uploading file: {response.text}")
    return None

def verify_proof(unique_id: str, proof: dict) -> bool:
    """Verify the proof with the server."""
    response = requests.post(
        f"{settings.SERVER_URL}/verify-proof/",
        json={"id": unique_id, "proof": proof}  
    )
    
    if response.status_code == 200:
        print("Proof verified successfully.")
        print(response.json())
        return True
    
    print(f"Error verifying proof: {response.text}")
    return False

