import hashlib
from typing import Dict
from .config import settings
import logging

logger = logging.getLogger(__name__)

def verify_proof(y: int, checksum: str, proof: dict) -> bool:
    """
    Verify the Zero-Knowledge Proof provided by the client.

    Args:
        y (int): The client's public key.
        checksum (str): The checksum of the uploaded file.
        proof (dict): The proof containing 'commitment' and 'response'.

    Returns:
        bool: True if the proof is valid, False otherwise.
    """
    commitment = proof.get("commitment")
    response = proof.get("response")
    
    if commitment is None or response is None:
        logger.debug("Proof is missing 'commitment' or 'response'.")
        return False

    # Compute the challenge c = Hash(checksum || commitment) mod p
    # Ensure consistent byte representation
    data = f"{checksum}{commitment}".encode()
    challenge = int(hashlib.sha256(data).hexdigest(), 16) % settings.ZKP_PRIME
    logger.debug(f"Computed challenge: {challenge} (Hash: {hashlib.sha256(data).hexdigest()})")

    # Compute expected_commitment = g^s * y^{-c} mod p
    try:
        y_inverse_c = pow(y, -challenge, settings.ZKP_PRIME)
    except ValueError:
        # If y and p are not coprime, inverse does not exist
        logger.debug("Modular inverse does not exist.")
        return False

    expected_commitment = (pow(settings.ZKP_GENERATOR, response, settings.ZKP_PRIME) * y_inverse_c) % settings.ZKP_PRIME
    logger.debug(f"Computed expected_commitment: {expected_commitment}")

    # Compare with the provided commitment
    verification_result = commitment == expected_commitment
    logger.debug(f"Verification result: {verification_result}")

    return verification_result

