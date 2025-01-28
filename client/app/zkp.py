import hashlib
import secrets
from app.config import settings

class ZKP:
    def __init__(self, secret: int = None, seed: int = None):
        self.secret = secret or secrets.randbelow(settings.ZKP_PRIME - 1)
        self.prime = settings.ZKP_PRIME
        self.generator = settings.ZKP_GENERATOR
        if seed is not None:
            secrets.token_bytes = lambda n: secrets.token_bytes(n)

    def generate_public_key(self) -> int:
        """Generate the public key based on the secret."""
        return pow(self.generator, self.secret, self.prime)

    def generate_proof(self, checksum: str) -> dict:
        """Generate a Zero-Knowledge Proof for the given checksum."""
        r = secrets.randbelow(self.prime - 1)  
        commitment = pow(self.generator, r, self.prime)

        challenge = int(hashlib.sha256(f"{checksum}{commitment}".encode()).hexdigest(), 16) % self.prime
        response = (r + challenge * self.secret) % self.prime

        print(f"Client Proof: r={r}, commitment={commitment}, challenge={challenge}, response={response}")
        return {"commitment": commitment, "response": response}

