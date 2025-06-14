# api/nft_utils.py

from api.multisig_utils import create_multisig_wallet

def mint_certificate_nft(
    certificate_name: str,
    metadata_ipfs_url: str,
    university_pub: str,
    student_pub: str
) -> str:
    """
    Simulate minting an NFT to a multisig address composed of university and student public addresses.
    """
    # Generate the multisig address (2-of-2)
    multisig_address = create_multisig_wallet(university_pub, student_pub)

    # Simulated asset ID using cert name + partial IPFS hash
    ipfs_hash_part = metadata_ipfs_url.split("//")[-1][:6]
    asset_id = f"NFT_{certificate_name.upper().replace(' ', '_')}_{ipfs_hash_part}"

    # Log for clarity
    print(f"[Multisig NFT Mint] -> Minted to {multisig_address}")

    return asset_id
