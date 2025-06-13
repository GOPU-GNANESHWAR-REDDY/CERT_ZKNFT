import os
from algosdk.atomic_transaction_composer import AtomicTransactionComposer
from algosdk.abi import Method
from algokit_utils import (
    Account,
    AlgorandClient,
    ApplicationClient,
    ApplicationSpecification,
    OnComplete,
    PayParams,
    TransactionParameters,
)
from algopy import (
    ARC4Contract,
    Asset,
    Global,
    Txn,
    UInt64,
    arc4,
    itxn,
    subroutine,
)

# --- 1. Smart Contract Definition (AssetMinter) ---
class AssetMinter(ARC4Contract):
    """
    A smart contract to control the creation and distribution of an ASA.
    The contract creator is the only one who can mint new tokens, and
    only whitelisted accounts can receive them.
    """

    def __init__(self) -> None:
        # The ID of the asset this contract controls
        self.asset_id = UInt64(0)
        # A mapping to store whitelisted addresses (address -> 1)
        self.whitelisted = arc4.DynamicArray[arc4.Address]()

    @arc4.abimethod(allow_actions=["NoOp"], create="require")
    def create_application(self) -> None:
        """Initializes the contract state. No logic needed on creation."""
        pass

    @arc4.abimethod
    def create_asset(self, unit_name: arc4.String, asset_name: arc4.String) -> UInt64:
        """
        Creates the ASA that this contract will manage.
        This can only be called once by the contract creator.
        """
        assert Txn.sender == Global.creator_address, "Only creator can create the asset"
        assert self.asset_id == 0, "Asset has already been created"

        # Create the asset using an inner transaction
        # The contract itself will be the manager, freeze, and clawback address
        payment = itxn.Payment(
            receiver=Global.current_application_address,
            amount=100_000,  # cover asset creation fee
            fee=0,
        )

        asset_creation = itxn.AssetConfig(
            total=10_000_000,
            decimals=2,
            unit_name=unit_name.native,
            asset_name=asset_name.native,
            manager=Global.current_application_address,
            freeze=Global.current_application_address,
            clawback=Global.current_application_address,
            fee=0,
        )
        itxn.submit_txns(payment, asset_creation)

        # Store the new asset's ID in global state
        self.asset_id = asset_creation.created_asset.id
        return self.asset_id

    @arc4.abimethod
    def whitelist(self, account: arc4.Address) -> None:
        """
        Adds an account to the whitelist.
        Only the contract creator can do this.
        """
        assert Txn.sender == Global.creator_address, "Only creator can whitelist addresses"
        self.whitelisted.append(account)

    @arc4.abimethod
    def mint(self, receiver: arc4.Account, amount: arc4.UInt64) -> None:
        """
        Mints (transfers) tokens from the contract's reserve to a whitelisted account.
        Only the contract creator can call this method.
        """
        assert Txn.sender == Global.creator_address, "Only creator can mint"
        
        # Verify the receiver is whitelisted
        is_whitelisted = False
        for i in range(self.whitelisted.size):
            if self.whitelisted[i] == receiver.native:
                is_whitelisted = True
                break
        assert is_whitelisted, "Receiver is not whitelisted"

        # Perform the asset transfer (mint)
        itxn.AssetTransfer(
            xfer_asset=Asset(self.asset_id),
            asset_receiver=receiver.native,
            asset_amount=amount.native,
            fee=0,
        ).submit()

    @arc4.abimethod(allow_actions=["OptIn"])
    def opt_in_to_asset(self, asset: arc4.Asset) -> None:
        """Allows the contract to opt-in to the asset it manages."""
        assert asset.id == self.asset_id, "Can only opt in to the contract's asset"
        itxn.AssetTransfer(
            xfer_asset=asset.native,
            asset_receiver=Global.current_application_address,
            asset_amount=0,
            fee=0
        ).submit()


# --- 2. Deployment and Interaction Script ---
def main() -> None:
    # --- Client and Account Setup ---
    print("--- 1. Initializing client and creating accounts... ---")
    client = AlgorandClient.default_localnet()
    creator = client.account.localnet_dispenser()
    test_account = client.account.localnet_dispenser()

    print(f"Creator Account: {creator.address}")
    print(f"Test Account: {test_account.address}")

    # --- Deploy the Contract ---
    print("\n--- 2. Deploying the AssetMinter Smart Contract... ---")
    # Get the contract specification
    app_spec = ApplicationSpecification.from_contract(AssetMinter())
    
    # Create an ApplicationClient
    app_client = ApplicationClient(client, app_spec, signer=creator.signer)

    # Deploy the app
    create_response = app_client.create(on_complete=OnComplete.NoOpOC, call_abi_method=False)
    print(f"✅ Contract deployed with App ID: {app_client.app_id}")
    
    # --- Fund the Contract Account ---
    # The contract needs ALGO to pay for inner transactions (like asset creation)
    app_client.fund(1 * 10**6) # Fund with 1 ALGO
    print("Funded contract with 1 ALGO.")

    # --- Create the ASA via the Smart Contract ---
    print("\n--- 3. Calling create_asset on the contract... ---")
    create_asset_response = app_client.call(
        "create_asset",
        unit_name="HTK",
        asset_name="Hackathon Token"
    )
    asset_id = create_asset_response.return_value
    print(f"✅ Asset created via contract. Asset ID: {asset_id}")
    
    # --- Whitelist the Test Account ---
    print(f"\n--- 4. Whitelisting the test account: {test_account.address} ---")
    app_client.call("whitelist", account=test_account.address)
    print("✅ Test account has been whitelisted.")

    # --- Test Account Opt-In ---
    # The test account must opt-in to receive the asset
    print("\n--- 5. Test account opting into the asset... ---")
    
    # The test account needs to sign this transaction
    test_signer = test_account.signer
    
    atc = AtomicTransactionComposer()
    atc.add_transaction(
        client.algod.suggested_params(),
        sender=test_account.address,
        signer=test_signer,
        receiver=test_account.address,
        amt=0,
        index=asset_id,
        type="axfer"
    )
    atc.execute(client.algod, 4)
    print(f"✅ Test account successfully opted into Asset ID: {asset_id}")


    # --- Mint Tokens to the Whitelisted Account ---
    print("\n--- 6. Minting 500 HTK to the whitelisted test account... ---")
    app_client.call(
        "mint",
        receiver=test_account.address,
        amount=500,
        # The asset needs to be in the foreign assets array to be used in an inner transaction
        transaction_parameters=TransactionParameters(foreign_assets=[asset_id])
    )
    print("✅ Mint successful!")
    
    # Check balance
    test_asset_info = client.algod.account_asset_info(test_account.address, asset_id)
    balance = test_asset_info['asset-holding']['amount']
    print(f"Test account final balance: {balance} HTK")
    
    # --- (Optional) Demonstrate a failed mint to a non-whitelisted account ---
    print("\n--- 7. Demonstrating failed mint to a non-whitelisted account... ---")
    non_whitelisted_account = client.account.localnet_dispenser()
    print(f"New non-whitelisted account: {non_whitelisted_account.address}")
    try:
        app_client.call(
            "mint",
            receiver=non_whitelisted_account.address,
            amount=100,
            transaction_parameters=TransactionParameters(foreign_assets=[asset_id])
        )
    except Exception as e:
        print(f"❌ Transaction failed as expected!")
        print("   Error message contains: 'Receiver is not whitelisted'")


if __name__ == "__main__":
    # To run this script, you need to have a running Algorand local network.
    # You can set one up easily using AlgoKit: `algokit localnet start`
    if "VITE_HELLO_WORLD_APP_ID" in os.environ:
        del os.environ["VITE_HELLO_WORLD_APP_ID"]
    main()