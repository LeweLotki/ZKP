# client/client/zkp.py

import hashlib
from typing import Dict
import secrets
from config import settings

class ZKP:
    def __init__(self, secret: int = None):
        """
        Initialize the ZKP instance with a secret.
        If no secret is provided, generate a random one within [1, PRIME-1].

        Args:
            secret (int, optional): The secret key. Defaults to None.
        """
        self.secret = secret or secrets.randbelow(settings.ZKP_PRIME - 1) + 1  # Ensure secret is in [1, PRIME-1]
        self.prime = settings.ZKP_PRIME
        self.generator = settings.ZKP_GENERATOR

    def generate_public_key(self) -> int:
        """
        Generate the public key based on the secret.

        Returns:
            int: The public key.
        """
        return pow(self.generator, self.secret, self.prime)

    def generate_proof(self, checksum: str) -> Dict[str, int]:
        """
        Generate a Zero-Knowledge Proof (ZKP) for the given checksum.

        Args:
            checksum (str): The checksum of the file.

        Returns:
            Dict[str, int]: A dictionary containing 'commitment' and 'response'.
        """
        # Choose random r
        r = secrets.randbelow(self.prime - 1) + 1
        # Compute commitment t = g^r mod p
        t = pow(self.generator, r, self.prime)
        
        # Compute challenge c = Hash(t || checksum) mod p
        checksum_bytes = bytes.fromhex(checksum)
        t_bytes = t.to_bytes((t.bit_length() + 7) // 8, byteorder='big')
        hasher = hashlib.sha256()
        hasher.update(t_bytes + checksum_bytes)
        c = int(hasher.hexdigest(), 16) % self.prime
        
        # Compute response s = r + c * x mod p
        s = (r + c * self.secret) % self.prime

        # Debug statements (use logging in production)
        print(f"Client Computation: commitment={t}, response={s}, challenge={c}")
        print(f"Client Params: prime={self.prime}, generator={self.generator}, secret={self.secret}")

        return {
            "commitment": t,
            "response": s
        }

