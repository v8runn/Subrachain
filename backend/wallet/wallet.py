import json
import uuid
import ecdsa
import hashlib

from backend.config import STARTING_BALANCE

class Wallet:
    """
    An individual wallet for a miner.
    Keeps track of the miner's balance.
    Allows a miner to authorize transactions.
    """
    def __init__(self):
        self.address = str(uuid.uuid4())[0:8]
        self.balance = STARTING_BALANCE
        self.private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.public_key = self.private_key.get_verifying_key()

    def sign(self, data):
        """
        Generate a signature based on the data using the local private key.
        """
        return self.private_key.sign(json.dumps(data).encode('utf-8'), hashfunc=hashlib.sha256)

    @staticmethod
    def verify(public_key, data, signature):
        """
        Verify a signature based on the original public key and data.
        """
        try:
            verifying_key = ecdsa.VerifyingKey.from_string(public_key.to_string(), curve=ecdsa.SECP256k1)
            return verifying_key.verify(signature, json.dumps(data).encode('utf-8'), hashfunc=hashlib.sha256)
        except ecdsa.BadSignatureError:
            return False

def main():
    wallet = Wallet()
    print(f'wallet.__dict__: {wallet.__dict__}')

    data = { 'foo': 'bar' }
    signature = wallet.sign(data)
    print(f'signature: {signature}')

    should_be_valid = Wallet.verify(wallet.public_key, data, signature)
    print(f'should_be_valid: {should_be_valid}')

    should_be_invalid = Wallet.verify(Wallet().public_key, data, signature)
    print(f'should_be_invalid: {should_be_invalid}')

if __name__ == '__main__':
    main()

