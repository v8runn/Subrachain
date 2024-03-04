import json
import uuid
import ecdsa
import hashlib
from backend.config import STARTING_BALANCE

class Wallet:
    def __init__(self, blockchain=None):
        self.blockchain = blockchain
        self.address = str(uuid.uuid4())[0:8]
        self.private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.public_key = self.private_key.get_verifying_key()
        self.serialize_public_key()

    @property
    def balance(self):
            return Wallet.calculate_balance(self.blockchain, self.address)

    def sign(self, data):
        return self.private_key.sign(json.dumps(data).encode('utf-8'), hashfunc=hashlib.sha256).hex()

    def serialize_public_key(self):
        self.public_key = self.public_key.to_pem().decode('utf-8')

    @staticmethod
    def verify(public_key_pem, data, signature_hex):
        try:
            verifying_key = ecdsa.VerifyingKey.from_pem(public_key_pem)
            return verifying_key.verify(bytes.fromhex(signature_hex), json.dumps(data).encode('utf-8'), hashfunc=hashlib.sha256)
        except ecdsa.BadSignatureError:
            return False
        

    @staticmethod
    def calculate_balance(blockchain, address):
        balance = STARTING_BALANCE

        if not blockchain:
            return balance

        for block in blockchain.chain:
            for transaction in block.data:
                if transaction['input']['address'] == address:
                    balance = transaction['output'][address]
                elif address in transaction['output']:
                    balance += transaction['output'][address]

        return balance

def main():
    wallet = Wallet()
    print(f'wallet.__dict__: {wallet.__dict__}')

    data = {'hello': 'world'}
    signature = wallet.sign(data)
    print(f'signature: {signature}')

    should_be_valid = Wallet.verify(wallet.public_key, data, signature)
    print(f'should_be_valid: {should_be_valid}')

    another_wallet = Wallet()
    should_be_invalid = Wallet.verify(another_wallet.public_key, data, signature)
    print(f'should_be_invalid: {should_be_invalid}')

if __name__ == '__main__':
    main()
