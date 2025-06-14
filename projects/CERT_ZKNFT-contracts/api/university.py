from fastapi import APIRouter
from pydantic import BaseModel
from api.auth import generate_profile_id
from api.ipfs_utils import upload_to_ipfs
from api.nft_utils import mint_certificate_nft
from api.qr_utils import generate_qr
from api.zkp_utils import verify_zk_proof
from api.utils.storage import save_to_file, load_from_file, save_students
from api.student import student_profiles, STUDENT_DB_FILE

router = APIRouter()

DB_FILE = "data/universities.json"
university_profiles = load_from_file(DB_FILE)

# ----------- 7.1: Create University Profile -----------

class UniversityCreateRequest(BaseModel):
    name: str

@router.post("/university/create-profile")
def create_university_profile(data: UniversityCreateRequest):
    for uid, profile in university_profiles.items():
        if profile["name"].lower() == data.name.lower():
            return {"university_id": uid, "name": profile["name"]}

    university_id = generate_profile_id("university")
    university_profiles[university_id] = {
        "name": data.name,
        "certificates": []
    }
    save_to_file(university_profiles, DB_FILE)
    return {"university_id": university_id, "name": data.name}


# ----------- 7.1.1: Mint Certificate -----------

class CertRequest(BaseModel):
    university_id: str
    university_pub: str
    student_name: str
    student_pub: str
    course: str
    grade: str

@router.post("/university/mint-certificate")
def mint_certificate(data: CertRequest):
    cert_metadata = {
        "student_name": data.student_name,
        "course": data.course,
        "grade": data.grade,
        "issuer": data.university_id
    }

    ipfs_url = upload_to_ipfs(cert_metadata)
    asset_id = mint_certificate_nft(
        certificate_name=f"{data.student_name}_{data.course}",
        metadata_ipfs_url=ipfs_url,
        university_pub=data.university_pub,
        student_pub=data.student_pub
    )

    if data.university_id in university_profiles:
        certs = university_profiles[data.university_id]["certificates"]
        for cert in certs:
            if cert["student"] == data.student_name and cert["course"] == data.course:
                return {
                    "status": "Certificate already exists",
                    "asset_id": cert["nft_asset"],
                    "ipfs_url": cert["ipfs"]
                }

        certs.append({
            "student": data.student_name,
            "course": data.course,
            "nft_asset": asset_id,
            "ipfs": ipfs_url,
            "university_pub": data.university_pub,
            "student_pub": data.student_pub
        })
        save_to_file(university_profiles, DB_FILE)

    return {
        "status": "Certificate minted",
        "asset_id": asset_id,
        "ipfs_url": ipfs_url
    }


# ----------- 7.1.2 & 7.1.3: Share Certificate -----------

class CertShareRequest(BaseModel):
    university_id: str
    student_id: str
    nft_asset_id: str

@router.post("/university/share-certificate")
def share_certificate(data: CertShareRequest):
    certs = university_profiles.get(data.university_id, {}).get("certificates", [])

    cert = next((c for c in certs if c["nft_asset"] == data.nft_asset_id), None)
    if not cert:
        return {"error": "Certificate not found"}

    # Check if already shared
    if cert.get("student_id") == data.student_id and "qr_token" in cert:
        return {
            "status": "Already assigned",
            "qr_path": cert["qr_token"]
        }

    # 🔐 Generate QR
    qr_data = f"{data.student_id}|{data.nft_asset_id}|{data.university_id}"
    qr_path = generate_qr(qr_data, filename=f"{data.student_id}_{data.nft_asset_id}.png")

    cert["student_id"] = data.student_id
    cert["qr_token"] = qr_path

    # Sync to student without duplicates
    if data.student_id in student_profiles:
        student_certs = student_profiles[data.student_id]["certificates"]

        # Replace existing cert if it already exists
        updated = False
        for i, existing_cert in enumerate(student_certs):
            if existing_cert["nft_asset"] == cert["nft_asset"]:
                student_certs[i] = cert
                updated = True
                break

        # If not found, append new
        if not updated:
            student_certs.append(cert)

        save_students(student_profiles, STUDENT_DB_FILE)

    # Save university profile as well
    save_to_file(university_profiles, DB_FILE)

    return {
        "status": "QR Token generated and assigned",
        "qr_path": qr_path
    }



# ----------- 7.1.4: Verify ZK Proof -----------

class CertVerifyRequest(BaseModel):
    university_id: str
    student_id: str
    nft_asset_id: str
    zk_proof: str

@router.post("/university/verify-certificate")
def verify_certificate(data: CertVerifyRequest):
    university = university_profiles.get(data.university_id)
    if not university:
        return {"status": "University not found", "valid": False}

    certs = university.get("certificates", [])
    cert = next(
        (c for c in certs if c.get("student_id") == data.student_id and c.get("nft_asset") == data.nft_asset_id),
        None
    )

    if not cert:
        return {"status": "Certificate not found", "valid": False}

    expected_hash = cert["ipfs"].split("//")[-1]
    is_valid = verify_zk_proof(data.zk_proof, expected_hash)

    return {
        "status": "Verification complete" if is_valid else "Invalid proof",
        "valid": is_valid,
        "certificate": cert if is_valid else None
    }


# ----------- Debug View -----------

@router.get("/university/debug-view/{university_id}")
def debug_view(university_id: str):
    return university_profiles.get(university_id, {})
