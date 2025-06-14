# api/multisig_utils.py

from algosdk.transaction import Multisig

def create_multisig_wallet(pub1: str, pub2: str, threshold: int = 2) -> str:
    """
    Create a multisig wallet from two public addresses.
    Threshold: how many of the addresses are needed to sign.
    Returns: multisig address string.
    """
    msig = Multisig(
        version=1,
        threshold=threshold,
        addresses=[pub1, pub2]
    )
    return msig.address()


def get_multisig_object(pub1: str, pub2: str, threshold: int = 2) -> Multisig:
    """
    Return the full Multisig object (for transactions).
    """
    return Multisig(version=1, threshold=threshold, addresses=[pub1, pub2])
