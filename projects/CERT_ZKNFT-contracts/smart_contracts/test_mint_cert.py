import os
from dotenv import load_dotenv
from algokit_utils import AlgorandClient, Account
from smart_contracts.artifacts.cert_zknft.cert_zknft_client import CertZknftClient

# Load environment variables
load_dotenv()
mnemonic = os.getenv("DEPLOYER_MNEMONIC")

if not mnemonic:
    raise Exception("❌ Missing DEPLOYER_MNEMONIC in .env")

# Create Algorand client (use localnet or testnet)
algorand = AlgorandClient.default_localnet()

# ✅ FIXED: Get deployer account
deployer = Account.from_mnemonic(mnemonic)

# The deployed App ID (your deployed app ID from previous steps)
APP_ID = 741185751

# Create smart contract client instance
app_client = CertZknftClient(algorand.client.algod, app_id=APP_ID, sender=deployer)

# Call the mint_cert method
result = app_client.mint_cert(student="Alice", course="Blockchain 101")

# Print result
print("🎓 Smart contract response:", result.return_value)
