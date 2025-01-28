import hashlib
import secrets
from app.config import settings

class ZKP:
    def __init__(self, secret: int = None):
        # Use secret or generate a random secret based on the prime
        self.secret = secret or secrets.randbelow(settings.ZKP_PRIME - 1)
        self.prime = settings.ZKP_PRIME
        self.generator = settings.ZKP_GENERATOR

    def generate_public_key(self) -> int:
        """Generate the public key based on the secret."""
        return pow(self.generator, self.secret, self.prime)

    def generate_proof(self, checksum: str) -> dict:
        """
        Generate a Zero-Knowledge Proof (ZKP) for the given checksum.
        
        Returns:
            A dictionary containing the commitment, response, and public_key.
        """
        r = secrets.randbelow(self.prime - 1)  # Ensure r is within [1, p-1]
        commitment = pow(self.generator, r, self.prime)  # t = g^r mod p

        # Calculate challenge using checksum and commitment
        challenge = int(hashlib.sha256(f"{checksum}{commitment}".encode()).hexdigest(), 16) % self.prime

        # Calculate response using r and challenge
        response = (r + challenge * self.secret) % self.prime

        print(f"Server Proof: r={r}, commitment={commitment}, challenge={challenge}, response={response}")
        return {"commitment": commitment, "response": response}

    def verify_proof(self, public_key: int, checksum: str, proof: dict) -> bool:
        """
        Verify the Zero-Knowledge Proof (ZKP).
        """
        commitment = proof["commitment"] % self.prime
        response = proof["response"] % self.prime

        # Calculate challenge using checksum and commitment
        challenge = int(hashlib.sha256(f"{checksum}{commitment}".encode()).hexdigest(), 16) % self.prime

        print(f"Server Verification: commitment={commitment}, response={response}, challenge={challenge}")

        try:
            # Compute expected commitment: t' = (g^s mod p) * (y^(-c) mod p) mod p
            expected_commitment = (
                pow(self.generator, response, self.prime) *
                pow(public_key, self.prime - 1 - challenge, self.prime)  # Modular inverse
            ) % self.prime
            print(f"Expected Commitment: {expected_commitment}")
        except ValueError as e:
            print(f"Error in modular arithmetic: {e}")
            return False

        return commitment == expected_commitment

