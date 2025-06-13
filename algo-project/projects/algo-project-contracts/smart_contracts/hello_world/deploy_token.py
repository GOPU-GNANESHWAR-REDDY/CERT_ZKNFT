from algokit_utils import (
    Account,
    ApplicationSpecification,
    get_algod_client,
    get_indexer_client,
    deploy_app,
    get_localnet_default_account,
)

def deploy():
    # Get the default account from localnet
    account = get_localnet_default_account()
    
    # Get the algod client
    algod_client = get_algod_client()
    
    # Deploy the contract
    app_spec = ApplicationSpecification.from_json("artifacts/token_contract.json")
    
    # Deploy the application
    app_client = deploy_app(
        algod_client,
        app_spec,
        account,
    )
    
    # Create the token
    result = app_client.call(
        "create_token",
        name="Hackathon Token",
        unit="HTK",
        total=1000000,  # 1 million tokens
        decimals=6
    )
    
    # Get the asset ID from the result
    asset_id = result.return_value
    
    print(f"Token created with Asset ID: {asset_id}")
    
    # Transfer some tokens to another address
    # Replace RECEIVER_ADDRESS with the address you want to send tokens to
    transfer_result = app_client.call(
        "transfer_token",
        asset_id=asset_id,
        receiver="TUSMJCP6XCC6JN7YUWI5CSZ4LP5E4HQ6EGLLXNVQIZCRD2NPPYQD35LVQE",  # Replace this with actual address
        amount=100000  # 100 tokens (considering 6 decimals)
    )
    
    print(f"Transfer transaction ID: {transfer_result.tx_id}")

if __name__ == "__main__":
    deploy()