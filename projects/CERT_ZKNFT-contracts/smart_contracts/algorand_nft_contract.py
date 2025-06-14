# Purpose: Smart contract logic for NFT creation + compliance
# Compatible with ARC3/ARC69 for CERT-ZKNFT project
# ============================

from beaker import Application, ApplicationStateValue, GlobalStateSchema, sandbox, localnet, opt_in
from beaker.decorators import external, create
from pyteal import abi, Bytes, Txn, App, Assert

class CertZKNFT(Application):
    # Global state for keeping metadata
    next_cert_id = ApplicationStateValue(abi.Uint64)

    def __init__(self):
        super().__init__(
            name="CertZKNFT",
            state=GlobalStateSchema(num_uints=1, num_byte_slices=0),
        )

    @create
    def create(self):
        return self.next_cert_id.set(0)

    @external
    def mint_certificate(
        self,
        student: abi.Address,
        metadata_url: abi.String,  # IPFS or URL to JSON metadata
        cert_id: abi.Uint64,
        *,
        output: abi.Uint64
    ):
        # Only creator can mint
        creator = App.globalGet(Bytes("creator"))
        Assert(Txn.sender() == creator)

        # Asset creation transaction logic is handled off-chain
        # Here we just keep a record in the app
        key = Bytes("cert_").concat(abi.Uint64(cert_id).encode())
        App.globalPut(key, student.get())
        output.set(cert_id)

    @external(read_only=True)
    def check_ownership(
        self, cert_id: abi.Uint64, wallet: abi.Address, *, output: abi.Bool
    ):
        key = Bytes("cert_").concat(cert_id.encode())
        current_owner = App.globalGetEx(App.id(), key)
        output.set(current_owner.value() == wallet.get())

    @external(read_only=True)
    def get_next_cert_id(self, *, output: abi.Uint64):
        output.set(self.next_cert_id.get())

    @external
    def increment_cert_id(self):
        current = self.next_cert_id.get()
        return self.next_cert_id.set(current + Int(1))


# Usage hint (from CLI)
# - Compile with `algokit compile`
# - Deploy using `ApplicationClient`
# - Mint NFTs by calling `mint_certificate()` with university wallet

app = CertZKNFT()
