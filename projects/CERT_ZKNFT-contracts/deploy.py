import os
from algokit_utils.algorand import AlgorandClient
from algokit_utils import AlgoAmount
from dotenv import load_dotenv
from smart_contracts.artifacts.cert_zknft.cert_zknft_client import CertZKNFTFactory
# Import the generated client classes
from smart_contracts.artifacts.certificate_zknft.certificate_zknft_client import (
    CertificateZKNFTFactory,
)

# Load environment variables from .env
load_dotenv()

ALGOD_URL = os.getenv("ALGOD_URL")
ALGOD_TOKEN = os.getenv("ALGOD_TOKEN")
MNEMONIC = os.getenv("DEPLOYER_MNEMONIC")

if None in [ALGOD_URL, ALGOD_TOKEN, MNEMONIC]:
    raise Exception("❌ Missing environment variable. Check your .env file.")

# Set up Algorand client
algorand = AlgorandClient.default_local_net()  # Or use from_environment() for more flexibility

# Get deployer account from mnemonic
deployer = algorand.account.from_mnemonic(MNEMONIC, min_funds=AlgoAmount.algo(1))

print(f"🔑 Wallet: {deployer.address}")
print("🔎 Balance:", algorand.client.algod.account_info(deployer.address)["amount"], "microAlgos")

# Create the typed app factory
factory = algorand.client.get_typed_app_factory(
    CertificateZKNFTFactory, default_sender=deployer.address
)

# Deploy the contract idempotently
app_client, result = factory.deploy()

print("🚀 Deploying smart contract...")
print(f"✅ Deployed successfully")
print(f"📎 App ID: {app_client.app_id}")
print(f"📍 App Address: {app_client.app_address}")