import json
from algokit_utils import (
    AlgoAmount,
    AlgorandClient,
    AssetCreateParams,
    AssetTransferParams,
    OnSchemaBreak,
    OnUpdate,
    PaymentParams,
    SigningAccount,
)

def main():
    # Initialize the client
    algorand_client = AlgorandClient.default_localnet()
    
    # Get the account using the recommended method
    creator_account = algorand_client.account.localnet_dispenser()
    print(f"Creator account: {creator_account.address}")
    
    # Create a signing account with the private key
    signer = SigningAccount(private_key=creator_account.private_key)
    
    # Set the default signer
    algorand_client.set_default_signer(signer)

    # --- 1. Define Metadata ---
    # ARC-53 compliant metadata as a dictionary
    metadata = {
        "description": "This is a token created for the hackathon!",
        "image": "ipfs://bafkreibi4wzdwgypkyb764fmpnllbflaogimctinmymctzrcs4hp7afk7e", # Example IPFS CID
        "mimetype": "image/png",
    }
    
    # Encode the metadata dictionary to a JSON string, then to bytes
    metadata_note = json.dumps(metadata).encode()

    # --- 2. Create the Token with Metadata and Controls ---
    create_result = algorand_client.send.asset_create(
        AssetCreateParams(
            sender=creator_account.address,
            total=10_000_000,
            decimals=6,
            unit_name="HTK",
            asset_name="Hackathon Token",
            # --- Asset Controls ---
            manager=creator_account.address, # Can change control addresses
            reserve=creator_account.address, # Holds non-circulating supply
            freeze=creator_account.address,  # Can freeze/unfreeze tokens in user accounts
            clawback=creator_account.address, # Can revoke tokens from user accounts
            # --- Metadata ---
            url=f"https://gateway.pinata.cloud/ipfs/{metadata['image'].replace('ipfs://', '')}", # Direct link to asset (ARC-3)
            note=metadata_note # ARC-53 metadata
        )
    )
    
    asset_id = create_result.asset_id
    asset_name = create_result.confirmation['txn']['txn']['apar']['an']
    
    print(f"✅ Token created successfully!")
    print(f"   - Asset ID: {asset_id}")
    print(f"   - Asset Name: {asset_name}")
    print(f"   - Transaction ID: {create_result.tx_id}")
    print(f"   - Metadata Note: {metadata_note.decode()}")
    print(f"   - Control Addresses (Manager, Freeze, Clawback, Reserve) set to: {creator_account.address}")


if __name__ == "__main__":
    main()