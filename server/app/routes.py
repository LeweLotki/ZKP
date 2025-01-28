from fastapi import APIRouter, UploadFile, HTTPException, Form
from app.zkp import ZKP
from app.utils import save_file, calculate_checksum
from app.database import SessionLocal
from app import crud
import uuid
from pydantic import BaseModel

router = APIRouter()

# Initialize ZKP instance
zkp_server = ZKP()
server_public_key = zkp_server.generate_public_key()

@router.post("/upload-csv/")
async def upload_csv(file: UploadFile, public_key: str = Form(...)):
    """
    Endpoint to upload a CSV file and store its checksum and public key in the database.
    """
    unique_id = str(uuid.uuid4())
    try:
        # Save file and calculate checksum
        file_path = save_file(file, unique_id)
        checksum = calculate_checksum(file_path)

        # Store checksum and client's public key in the database
        db = SessionLocal()
        crud.add_client_data(db, unique_id, checksum, int(public_key))

        return {"message": "File uploaded and checksum saved.", "id": unique_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        db.close()

class ProofRequest(BaseModel):
    id: str
    proof: dict

@router.post("/verify-proof/")
async def verify_proof(proof_request: ProofRequest):
    """
    Endpoint to verify the Zero-Knowledge Proof.
    """
    unique_id = proof_request.id
    proof = proof_request.proof

    db = SessionLocal()
    client_data = crud.get_client_data(db, unique_id)
    
    if client_data is None:
        raise HTTPException(status_code=404, detail="ID not found.")
    
    server_checksum = client_data.checksum
    client_public_key = client_data.public_key
    
    if not zkp_server.verify_proof(client_public_key, server_checksum, proof):
        raise HTTPException(status_code=400, detail="Proof verification failed.")
    
    return {"status": "Proof verified successfully."}

