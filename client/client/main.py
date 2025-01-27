import hashlib
import requests
import secrets
import uuid

SERVER_URL = "http://127.0.0.1:8000"

def calculate_checksum(file_path: str) -> str:
    """Calculate the SHA-256 checksum of the given file."""
    with open(file_path, "rb") as f:
        file_content = f.read()
        return hashlib.sha256(file_content).hexdigest()


class ZKP:
    def __init__(self, secret: int = None):
        self.secret = secret or secrets.randbelow(2**256)  
        # Ensure that the prime and generator match the server's parameters
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
        """Generate the public key based on the secret."""
        return pow(self.generator, self.secret, self.prime)
    
    def generate_proof(self, checksum: str) -> dict:
        """
        Generate a Zero-Knowledge Proof (ZKP) for the given checksum.
        
        Returns:
            A dictionary containing the commitment and response.
        """
        r = secrets.randbelow(self.prime)  
        commitment = pow(self.generator, r, self.prime)  
        challenge = int(hashlib.sha256(f"{checksum}{commitment}".encode()).hexdigest(), 16) % self.prime  
        response = (r + challenge * self.secret) % self.prime  

        # Debug statements (consider using logging in production)
        print(f"Client Computation: commitment={commitment}, response={response}, challenge={challenge}")
        print(f"Client Params: prime={self.prime}, generator={self.generator}, secret={self.secret}")

        return {
            "commitment": commitment,
            "response": response
        }


def main():
    # Path to the CSV file to be uploaded
    file_path = "data.csv"
    
    # Calculate the checksum of the file
    checksum = calculate_checksum(file_path)
    print(f"Checksum: {checksum}")
    
    # Initialize the ZKP client
    zkp_client = ZKP()
    
    # Generate the public key
    client_public_key = zkp_client.generate_public_key()
    print(f"Client Public Key: {client_public_key}")
    
    # Upload the CSV file to the server along with the client's public key
    with open(file_path, "rb") as file:
        response = requests.post(
            f"{SERVER_URL}/upload-csv/",
            files={"file": file},
            data={"public_key": str(client_public_key)}  # Send as string form field
        )
    
    # Handle the server's response
    if response.status_code != 200:
        print(f"Failed to upload file with public key: {response.text}")
        return
    
    server_response = response.json()
    print("Server Response:", server_response)
    
    # Extract necessary information from the server's response
    unique_id = server_response.get("id")
    
    if not unique_id:
        print("Invalid server response: Missing 'id'.")
        return
    
    # Generate the proof using the checksum
    proof = zkp_client.generate_proof(checksum)
    
    # Prepare the proof request payload
    proof_request = {
        "id": unique_id,
        "proof": proof
    }
    
    # Send the proof to the server for verification
    proof_response = requests.post(
        f"{SERVER_URL}/verify-proof/",
        json=proof_request
    )
    
    # Handle the server's proof verification response
    if proof_response.status_code == 200:
        print("Proof Verification Response:", proof_response.json())
    else:
        print(f"Proof verification failed: {proof_response.text}")


if __name__ == "__main__":
    main()

