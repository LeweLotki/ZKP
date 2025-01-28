from app.utils import calculate_checksum, upload_file, verify_proof
from app.zkp import ZKP
from app.config import settings

def main():
    file_path = "data/data.csv"
    seed = 42     
    checksum = calculate_checksum(file_path)
    print(f"File Checksum: {checksum}")
    
    zkp_client = ZKP(seed=seed) 
    client_public_key = zkp_client.generate_public_key()
    print(f"Client Public Key: {client_public_key}")
    
    unique_id = upload_file(file_path, client_public_key)
    if not unique_id:
        print("Failed to upload the file. Exiting.")
        return

    print(f"File uploaded successfully. Unique ID: {unique_id}")
    
    proof = zkp_client.generate_proof(checksum)
    print(f"Generated Proof: {proof}")
    
    proof_verified = verify_proof(unique_id, proof)
    if proof_verified:
        print("Proof verification succeeded.")
    else:
        print("Proof verification failed.")

if __name__ == "__main__":
    main()

