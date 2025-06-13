import logging

import algokit_utils
from algokit_utils import Account

logger = logging.getLogger(__name__)


# define deployment behaviour based on supplied app spec
def deploy() -> None:
    # Import the generated client for the AssetMinter contract
    from smart_contracts.artifacts.asset_minter.asset_minter_client import (
        AssetMinterFactory,
        CreateAssetArgs,
        WhitelistArgs,
    )

    algorand = algokit_utils.AlgorandClient.from_environment()

    # Get accounts from the environment file
    deployer = algorand.account.from_environment("DEPLOYER")
    receiver = algorand.account.from_environment("RECEIVER") # Account to be whitelisted

    logger.info(f"Deployer: {deployer.address}")
    logger.info(f"Receiver: {receiver.address}")


    # Get the factory for the AssetMinter contract
    factory = algorand.client.get_typed_app_factory(
        AssetMinterFactory, default_sender=deployer.address
    )

    # Deploy the contract
    app_client, result = factory.deploy(
        on_update=algokit_utils.OnUpdate.AppendApp,
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
    )

    # Perform initial setup only when the app is first created
    if result.operation_performed == algokit_utils.OperationPerformed.Create:
        logger.info("New app created, performing initial setup...")
        
        # 1. Fund the contract so it can pay for inner transactions
        algorand.send.payment(
            algokit_utils.PaymentParams(
                amount=algokit_utils.AlgoAmount(algo=1),
                sender=deployer.address,
                receiver=app_client.app_address,
            )
        )
        logger.info(f"Funded contract {app_client.app_id} with 1 ALGO.")

        # 2. Call the create_asset method on the contract
        response = app_client.send.create_asset(
            args=CreateAssetArgs(unit_name="HTK", asset_name="Hackathon Token")
        )
        asset_id = response.abi_return
        logger.info(
            f"Called create_asset on {app_client.app_name} ({app_client.app_id}), "
            f"created Asset ID: {asset_id}"
        )
        
        # 3. Whitelist the receiver account
        app_client.send.whitelist(args=WhitelistArgs(account=receiver.address))
        logger.info(f"Whitelisted account: {receiver.address}")
        
    else:
        logger.info(f"Skipping setup for existing app: {app_client.app_id}")