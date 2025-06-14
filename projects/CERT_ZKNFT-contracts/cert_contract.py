from beaker.application import Application
from beaker.decorators import external
from beaker.lib.storage import GlobalStateValue
from pyteal import abi

class CertificateZKNFT(Application):
    certificate_count = GlobalStateValue(stack_type=abi.Uint64)

    @external
    def issue_certificate(self, *, output: abi.String):
        return output.set("✅ Certificate issued successfully")
