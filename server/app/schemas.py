from pydantic import BaseModel
from typing import Dict

class ProofRequest(BaseModel):
    id: str
    proof: Dict[str, int]  
