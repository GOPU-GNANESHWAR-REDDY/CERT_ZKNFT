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

    print(create_result)
    
    # Get the asset ID from the result
    asset_id = create_result.asset_id
    print(f"Token created with Asset ID: {asset_id}")
    
    # Create a second account for receiving tokens
    new_account = algorand_client.account.localnet_dispenser()
    print(f"Created new account: {new_account.address}")

    # receiver = algorand_client.account.get_account(sender=new_account.address)
    # receiver_signer = SigningAccount(private_key=receiver.private_key)
    
    # # Fund the receiver account with ALGOs so it can make transactions
    # algorand_client.send.payment(
    #     PaymentParams(
    #         sender=account.address,
    #         receiver=receiver.address,
    #         amount=AlgoAmount.algos(1),  # 1 ALGO should be plenty
    #     )
    # )
    
    # Have the receiver opt-in to the asset
    # algorand_client.set_default_signer(receiver_signer)
    opt_in_result = algorand_client.send.asset_transfer(
        AssetTransferParams(
            sender=new_account.address,
            receiver=new_account.address,  # Self-transfer for opt-in
            asset_id=asset_id,
            amount=0  # 0 amount for opt-in
        )
    )
    
    print(f"Opt-in transaction ID: {opt_in_result.tx_id}")
    
    # # Switch back to original signer for the transfer
    # algorand_client.set_default_signer(signer)
    
    # # Now transfer tokens to the receiver that has opted in
    # transfer_result = algorand_client.send.asset_transfer(
    #     AssetTransferParams(
    #         sender=account.address,
    #         receiver=receiver.address,
    #         asset_id=asset_id,
    #         amount=100_000  # 100 tokens
    #     )
    # )
    
    # print(f"Transfer transaction ID: {transfer_result.tx_id}")
    # print(f"Receiver address: {receiver.address}")

if __name__ == "__main__":
    main()