import json
import requests
import os

# Load these from .env or replace with your actual Pinata API keys
PINATA_API_KEY = os.getenv("PINATA_API_KEY") or "your_api_key"
PINATA_SECRET_API_KEY = os.getenv("PINATA_SECRET_API_KEY") or "your_secret_key"

PINATA_BASE_URL = "https://api.pinata.cloud/pinning/pinJSONToIPFS"


def upload_metadata_to_ipfs(metadata: dict) -> str:
    """
    Uploads metadata to IPFS via Pinata and returns the IPFS hash URL.
    """
    headers = {
        "Content-Type": "application/json",
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY
    }

    response = requests.post(PINATA_BASE_URL, data=json.dumps(metadata), headers=headers)

    if response.status_code == 200:
        ipfs_hash = response.json()["IpfsHash"]
        return f"ipfs://{ipfs_hash}"
    else:
        raise Exception(f"Failed to upload to IPFS: {response.text}")


# Example usage
if __name__ == "__main__":
    metadata = {
        "name": "Gnaneshwar B.Tech Certificate",
        "course": "AI/ML",
        "grade": "A+",
        "issued_by": "A1KQ1",
        "timestamp": "2025-06-14T12:00:00Z"
    }

    url = upload_metadata_to_ipfs(metadata)
    print("📡 IPFS URL:", url)
