# scripts/generate_accounts.py
from algosdk import account, mnemonic

def generate_account():
    private_key, address = account.generate_account()
    passphrase = mnemonic.from_private_key(private_key)

    print("🔐 Mnemonic:")
    print(passphrase)
    print("\n📬 Address:")
    print(address)

    return address

if __name__ == "__main__":
    print("University Account:")
    generate_account()
    print("\nStudent Account:")
    generate_account()
