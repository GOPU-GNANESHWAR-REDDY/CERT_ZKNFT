import os
from algosdk import account, mnemonic
from algosdk.v2client import algod
from dotenv import load_dotenv

from beaker.client import ApplicationClient
from cert_contract import CertificateZKNFT

# Load environment variables from .env
load_dotenv()

ALGOD_URL = os.getenv("ALGOD_URL")
ALGOD_TOKEN = os.getenv("ALGOD_TOKEN")
MNEMONIC = os.getenv("MNEMONIC")

# Validate environment
if None in [ALGOD_URL, ALGOD_TOKEN, MNEMONIC]:
    raise Exception("❌ Missing environment variable. Check your .env file.")

# Convert mnemonic to private key
private_key = mnemonic.to_private_key(MNEMONIC)
address = account.address_from_private_key(private_key)

# Algod Client
algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)

print(f"🔑 Wallet: {address}")
print("🔎 Balance:", algod_client.account_info(address)["amount"], "microAlgos")

# Deploy Smart Contract
app_client = ApplicationClient(
    client=algod_client,
    app=CertificateZKNFT(),
    signer=account.Account(private_key),
)

print("🚀 Deploying smart contract...")
app_id, app_addr, _ = app_client.create()

print(f"✅ Deployed successfully")
print(f"📎 App ID: {app_id}")
print(f"📍 App Address: {app_addr}")
