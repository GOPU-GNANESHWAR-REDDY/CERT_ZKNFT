# File: smart_contracts/nft_contract.py
"""
Handles Algorand Standard Asset (ASA) NFT minting logic.
This contract is independent of the app logic but can be invoked by it.
"""
from algosdk.v2client import algod
from algosdk import transaction, account


def create_nft(client: algod.AlgodClient, sender: str, private_key: str, nft_metadata_url: str):
    params = client.suggested_params()

    txn = transaction.AssetConfigTxn(
        sender=sender,
        sp=params,
        total=1,
        default_frozen=False,
        unit_name="ZKNFT",
        asset_name="ZK-Certificate NFT",
        manager=sender,
        reserve=sender,
        freeze=sender,
        clawback=sender,
        url=nft_metadata_url,
        decimals=0,
    )

    stxn = txn.sign(private_key)
    txid = client.send_transaction(stxn)
    transaction.wait_for_confirmation(client, txid, 4)

    ptx = client.pending_transaction_info(txid)
    asset_id = ptx["asset-index"]
    return asset_id


# File: smart_contracts/ipfs_utils.py
"""
Handles IPFS pinning logic using Pinata (or other services)
"""
import json
import requests

PINATA_BASE_URL = "https://api.pinata.cloud"
PIN_FILE_URL = f"{PINATA_BASE_URL}/pinning/pinJSONToIPFS"
HEADERS = {
    "pinata_api_key": "<YOUR_API_KEY>",
    "pinata_secret_api_key": "<YOUR_SECRET>",
}


def upload_metadata_to_ipfs(metadata: dict) -> str:
    response = requests.post(PIN_FILE_URL, headers=HEADERS, json={"pinataContent": metadata})
    if response.status_code == 200:
        ipfs_hash = response.json()["IpfsHash"]
        return f"ipfs://{ipfs_hash}"
    else:
        raise Exception("❌ Failed to upload metadata to IPFS:", response.text)
