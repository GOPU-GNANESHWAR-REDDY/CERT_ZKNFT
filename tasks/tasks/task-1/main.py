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
    account = algorand_client.account.localnet_dispenser()
    
    # Create a signing account with the private key
    signer = SigningAccount(private_key=account.private_key)
    
    # Set the default signer
    algorand_client.set_default_signer(signer)
    
    # Create the token
    create_result = algorand_client.send.asset_create(
        AssetCreateParams(
            sender=account.address,
            total=10_000_000,  # 10 million tokens
            decimals=6,
            default_frozen=False,
            unit_name="HTK",  # Hackathon Token
            asset_name="Hackathon Token",
        )
    )

    # print(create_result)
    
    # Get the asset ID from the result
    asset_id = create_result.asset_id
    asset_name = create_result.confirmation['txn']['txn']['apar']['an']
    print(f"Token created with Asset ID: {asset_id} and Asset Name: {asset_name}")
    
    # Create a second account for receiving tokens
    new_account = algorand_client.account.localnet_dispenser()
    print(f"Created new account: {new_account.address}")


    transaction_result = algorand_client.send.asset_transfer(
        AssetTransferParams(
            sender=new_account.address,
            receiver=new_account.address,  # Self-transfer for opt-in
            asset_id=asset_id,
            amount=0  # 0 amount for opt-in
        )
    )

    print(f"Transaction ID: {transaction_result.tx_id}")
    

if __name__ == "__main__":
    main()