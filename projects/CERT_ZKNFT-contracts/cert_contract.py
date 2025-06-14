from algopy import ARC4Contract, String, arc4

class CertificateZKNFT(ARC4Contract):
    @arc4.abimethod
    def mint_cert(self, student: String, course: String) -> String:
        # For demonstration, just return the student string as in your original logic
        return student