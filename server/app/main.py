from fastapi import FastAPI, UploadFile, HTTPException, Form
import hashlib
from pydantic import BaseModel
import os
from typing import Tuple, Dict
import secrets
import uuid

app = FastAPI()

class ProofRequest(BaseModel):
    id: str
    proof: dict  # Removed 'checksum' as it's stored on the server

class ZKP:
    def __init__(self, secret: int = None):
        self.secret = secret or secrets.randbelow(2**256)
        self.prime = int(
            "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E08"
            "8A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD"
            "3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6"
            "F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F241"
            "17C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D"
            "39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED"
            "529077096966D670C354E4ABC9804F1746C08CA237327FFFFFFFFFFFFFFFF",
            16
        )
        self.generator = 2

    def generate_public_key(self) -> int:
        return pow(self.generator, self.secret, self.prime)

    def generate_proof(self, checksum: str) -> Tuple[int, int]:
        r = secrets.randbelow(self.prime)
        commitment = pow(self.generator, r, self.prime)
        challenge = int(hashlib.sha256(f"{checksum}{commitment}".encode()).hexdigest(), 16) % self.prime
        response = (r + challenge * self.secret) % self.prime
        return commitment, response

    def verify_proof(self, public_key: int, checksum: str, proof: dict) -> bool:
        commitment = proof["commitment"]
        response = proof["response"]
        challenge = int(hashlib.sha256(f"{checksum}{commitment}".encode()).hexdigest(), 16) % self.prime
        expected_commitment = (pow(self.generator, response, self.prime) * pow(public_key, -challenge, self.prime)) % self.prime
        return commitment == expected_commitment

# In-memory storage for example purposes (Use a database for production)
checksums: Dict[str, str] = {}
client_public_keys: Dict[str, int] = {}
zkp_server = ZKP()
server_public_key = zkp_server.generate_public_key()

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile, public_key: str = Form(...)):
    """
    Endpoint to upload a CSV file along with the client's public key.
    """
    unique_id = str(uuid.uuid4())
    try:
        content = await file.read()
        file_path = f"uploads/{unique_id}.csv"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(content)
        checksum = hashlib.sha256(content).hexdigest()
        checksums[unique_id] = checksum
        client_public_keys[unique_id] = int(public_key)
        return {
            "message": "Checksum calculated and saved on server.",
            "id": unique_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/verify-proof/")
async def verify_proof(proof_request: ProofRequest):
    """
    Endpoint to verify the Zero-Knowledge Proof provided by the client.
    """
    unique_id = proof_request.id
    if unique_id not in checksums or unique_id not in client_public_keys:
        raise HTTPException(status_code=404, detail="Checksum or public key not found for the given ID.")
    server_checksum = checksums[unique_id]
    proof = proof_request.proof
    client_public_key = client_public_keys.get(unique_id)
    if not client_public_key:
        raise HTTPException(status_code=400, detail="Public key missing for the given ID.")
    verified = zkp_server.verify_proof(client_public_key, server_checksum, proof)
    if verified:
        return {"status": "OK"}
    raise HTTPException(status_code=400, detail="Proof verification failed")

