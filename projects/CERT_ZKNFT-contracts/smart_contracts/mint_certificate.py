# smart_contracts/mint_certificate.py

from pyteal import *

def approval_program():
    """
    This basic approval program approves any transaction.
    We'll evolve this logic in steps.
    """
    return Approve()

def clear_program():
    """
    Standard clear state logic that approves clear requests.
    """
    return Approve()

if __name__ == "__main__":
    # Compile to TEAL
    with open("artifacts/approval.teal", "w") as f:
        compiled = compileTeal(approval_program(), mode=Mode.Application, version=6)
        f.write(compiled)

    with open("artifacts/clear.teal", "w") as f:
        compiled = compileTeal(clear_program(), mode=Mode.Application, version=6)
        f.write(compiled)
from algopy import ARC4Contract, String, arc4

class CertificateZKNFT(ARC4Contract):
    @arc4.abimethod
    def mint_cert(self, student: String, course: String, grade: String, issue_date: String) -> String:
        return f"{student} completed {course} with {grade} on {issue_date}"
