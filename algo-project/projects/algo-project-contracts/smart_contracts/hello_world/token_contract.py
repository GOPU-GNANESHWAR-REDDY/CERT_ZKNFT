from algopy import ARC4Contract, String
from algopy.arc4 import abimethod

#@subroutine cehck

class HelloWorld(ARC4Contract):
    @abimethod()
    def hello(self, name: String) -> String:
        return "Hello, " + name


# algokit project run build
# algokit project build all (in frontend)