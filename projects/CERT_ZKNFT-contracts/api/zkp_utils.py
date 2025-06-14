# api/zkp_utils.py

def generate_zk_proof(student_id: str, university_id: str, cert_hash: str) -> str:
    """
    Stub: Simulate generating a ZK proof.
    """
    return f"zkp_proof_for_{student_id}_{university_id}_{cert_hash}"

def verify_zk_proof(proof: str, expected_hash: str) -> bool:
    """
    Stub: Simulate verifying a ZK proof.
    """
    return expected_hash in proof
