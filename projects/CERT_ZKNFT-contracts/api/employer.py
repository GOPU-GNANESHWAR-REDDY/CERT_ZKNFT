# api/employer.py

from fastapi import APIRouter
from pydantic import BaseModel
from api.auth import generate_profile_id
from typing import Dict

router = APIRouter()

# In-memory employer DB (you can persist this later too)
employer_profiles: Dict[str, Dict] = {}

class EmployerCreateRequest(BaseModel):
    name: str

@router.post("/employer/create-profile")
def create_employer(data: EmployerCreateRequest):
    for eid, emp in employer_profiles.items():
        if emp["name"].lower() == data.name.lower():
            return {"employer_id": eid, "name": emp["name"]}

    employer_id = generate_profile_id("employer")
    employer_profiles[employer_id] = {
        "name": data.name,
        "verified_certificates": []
    }
    return {"employer_id": employer_id, "name": data.name}


# ------------------ 7.3.1 + 7.3.2 ------------------

class EmployerVerifyRequest(BaseModel):
    employer_id: str
    university_id: str
    student_id: str
    nft_asset_id: str
    zk_proof: str

@router.post("/employer/verify-student-cert")
def verify_student_cert(data: EmployerVerifyRequest):
    from api.university import verify_certificate

    # Proxy the verification call to university's method
    result = verify_certificate(data)

    # Store result if valid
    if result.get("valid") and data.employer_id in employer_profiles:
        employer_profiles[data.employer_id]["verified_certificates"].append(result["certificate"])

    return result


@router.get("/employer/debug-view/{employer_id}")
def view_employer_data(employer_id: str):
    return employer_profiles.get(employer_id, {})
