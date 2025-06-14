# ==========================
# CERT_ZKNFT Main Contract
# Purpose: Handles NFT certificate minting + verification
# Tightly integrated with backend API at `api/university.py`
# and used by ApplicationClient from `deploy.py`
# ==========================

from algopy import ARC4Contract, Bytes, abi, itob, App, Txn, Global, Assert
from algopy.arc4 import abimethod


class CertZknft(ARC4Contract):
    @abimethod()
    def hello(self, name: abi.String) -> abi.String:
        return abi.String("Hello, ").concat(name)

    @abimethod(read_only=True)
    def check_certificate_ownership(self, wallet: abi.Address, cert_id: abi.Uint64) -> abi.Bool:
        """
        Check if a wallet owns a certificate NFT (on-chain check via local state).
        Key: 'nft_{cert_id}'
        """
        key = Bytes("nft_").concat(itob(cert_id))
        current_owner = App.localGet(wallet, key)
        return current_owner == wallet

    @abimethod()
    def store_certificate_owner(self, cert_id: abi.Uint64, student: abi.Address):
        """
        Store NFT ownership in the local state (key = nft_{cert_id})
        Only creator (university) can call this.
        """
        key = Bytes("nft_").concat(itob(cert_id))
        Assert(Txn.sender() == Global.creator_address())
        App.localPut(student, key, student)

    @abimethod()
    def revoke_certificate(self, cert_id: abi.Uint64, student: abi.Address):
        """
        Revoke an NFT certificate from a student's account.
        """
        key = Bytes("nft_").concat(itob(cert_id))
        Assert(Txn.sender() == Global.creator_address())
        App.localDel(student, key)

    @abimethod(read_only=True)
    def list_certificates_for_student(self, student: abi.Address) -> abi.String:
        """
        Return a summary string of all cert keys for a student.
        (Mocked behavior – real use requires off-chain scan or box storage)
        """
        return abi.String("Query local state externally for keys prefixed with 'nft_'")
