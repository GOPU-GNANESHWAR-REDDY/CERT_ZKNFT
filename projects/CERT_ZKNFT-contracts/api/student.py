# api/student.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict
from api.auth import generate_profile_id
from api.utils.storage import save_students, load_students

STUDENT_DB_FILE = "data/students.json"
student_profiles = load_students(STUDENT_DB_FILE)

router = APIRouter()

# 1. ---------------- Create Profile ----------------

class StudentCreateRequest(BaseModel):
    name: str

@router.post("/student/create-profile")
def create_student_profile(data: StudentCreateRequest):
    # Prevent duplicates
    for sid, profile in student_profiles.items():
        if profile["name"].lower() == data.name.lower():
            return {"student_id": sid, "name": profile["name"]}

    student_id = generate_profile_id("student")
    student_profiles[student_id] = {
        "name": data.name,
        "certificates": []
    }

    save_students(student_profiles, STUDENT_DB_FILE)  # ✅ Write to file

    return {"student_id": student_id, "name": data.name}


# 2. ---------------- View Certificates ----------------

@router.get("/student/view-certificates/{student_id}")
def view_certificates(student_id: str):
    student = student_profiles.get(student_id)
    if not student:
        return {"error": "Student not found"}

    return {
        "student_id": student_id,
        "name": student["name"],
        "certificates": student["certificates"]
    }


# 3. ---------------- Apply for Verification ----------------

class ApplicationRequest(BaseModel):
    student_id: str
    university_id: str
    nft_asset_id: str

@router.post("/student/apply-verification")
def apply_for_verification(data: ApplicationRequest):
    from api.zkp_utils import generate_zk_proof
    proof = generate_zk_proof(data.student_id, data.university_id, data.nft_asset_id)
    return {
        "status": "Proof generated for employer verification",
        "zk_proof": proof
    }
