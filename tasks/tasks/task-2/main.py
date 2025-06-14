import json
from algosdk.error import AlgodHTTPError
from algokit_utils import (
    AlgoAmount,
    AlgorandClient,
    AssetCreateParams,
    AssetFreezeParams,
    AssetTransferParams,
    PaymentParams,
    SigningAccount,
)

def main():
    # 1. Initialize client and creator account
    print("--- 1. Initializing client and creating accounts... ---")
    algorand_client = AlgorandClient.default_localnet()
    creator_account = algorand_client.account.localnet_dispenser()
    creator_signer = SigningAccount(private_key=creator_account.private_key)
    algorand_client.set_default_signer(creator_signer)
    print(f"Creator account: {creator_account.address}")

    # 2. Create the Token with Metadata and Controls
    print("\n--- 2. Creating Asset with Metadata and Role Controls... ---")
    metadata = {
        "description": "This is a token created for the hackathon!",
        "image": "ipfs://bafkreibi4wzdwgypkyb764fmpnllbflaogimctinmymctzrcs4hp7afk7e",
        "mimetype": "image/png",
    }
    metadata_note = json.dumps(metadata).encode()

    create_result = algorand_client.send.asset_create(
        AssetCreateParams(
            sender=creator_account.address,
            total=10_000_000,
            decimals=2,
            unit_name="HTK",
            asset_name="Hackathon Token",
            manager=creator_account.address,
            reserve=creator_account.address,
            freeze=creator_account.address,
            clawback=creator_account.address,
            # ---- CORRECTED LINE ----
            # Use the shorter, standard ipfs:// URI which is well within the 96-byte limit.
            url=metadata["image"],
            note=metadata_note
        )
    )
    asset_id = create_result.asset_id
    print(f"✅ ASA created successfully!")
    print(f"   - Asset ID: {asset_id}")
    print(f"   - Asset Name: {create_result.confirmation['txn']['txn']['apar']['an']}")
    print(f"   - Control Roles (Manager, Freeze, Clawback) set to: {creator_account.address}")

    # 3. Set up the test account
    print("\n--- 3. Setting up the test account... ---")
    test_account = algorand_client.account.localnet_dispenser()
    test_signer = SigningAccount(private_key=test_account.private_key)
    print(f"Test account: {test_account.address}")

    # Fund the test account so it can pay for transaction fees
    algorand_client.send.payment(
        PaymentParams(
            sender=creator_account.address,
            receiver=test_account.address,
            amount=AlgoAmount(algo=0.2),  # Changed from algos to algo
            # extra_fee=AlgoAmount(0.001)  # Changed from algos to algo        
    )
    )
    print(f"Funded test account with 1 ALGO.")

    # Have the test account opt-in to the asset
    algorand_client.send.asset_transfer(
        AssetTransferParams(
            sender=test_account.address,
            receiver=test_account.address,
            asset_id=asset_id,
            amount=0
        ),
    )
    print(f"Test account opted into Asset ID: {asset_id}")

    # 4. Transfer assets to the test account
    print("\n--- 4. Transferring 100 HTK to the test account... ---")
    transfer_result = algorand_client.send.asset_transfer(
        AssetTransferParams(
            sender=creator_account.address,
            receiver=test_account.address,
            asset_id=asset_id,
            amount=100
        )
    )
    print(f"Transfer successful. Transaction ID: {transfer_result.tx_id}")
    
    # # Check the balance (optional)
    # test_account_info = algorand_client.algod.account_asset_info(test_account.address, asset_id)
    # balance = test_account_info['asset-holding']['amount']
    # print(f"Test account balance: {balance} HTK")

    # 5. Demonstrate Clawback
    print("\n--- 5. Demonstrating CLAWBACK role... ---")
    print(f"Revoking all 100 HTK from {test_account.address} using the clawback address.")
    
    clawback_result = algorand_client.send.asset_transfer(
        AssetTransferParams(
            sender=creator_account.address, # The clawback address sends the transaction
            receiver=creator_account.address, # Tokens are sent back to the creator
            asset_id=asset_id,
            amount=100,
            clawback_target=test_account.address
        )
        # Note: The creator_signer (the default) is used, as it's the clawback address
    )
    
    print("✅ Clawback successful!")
    print(f"   - Clawback Transaction ID: {clawback_result.tx_id}")

    # Verify final balance
    # test_account_info_after = algorand_client.algod.account_asset_info(test_account.address, asset_id)
    # balance_after = test_account_info_after['asset-holding']['amount']
    # print(f"Test account final balance: {balance_after} HTK")


if __name__ == "__main__":
    main()