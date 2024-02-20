import requests
from backend.wallet.wallet import Wallet
import time

BASEURL='http://localhost:5000'

def get_blockchain():
    return requests.get(f'{BASEURL}/blockchain').json()

def get_blockchain_mine():
    return requests.get(f'{BASEURL}/blockchain/mine').json()

def post_wallet_transaction(recipient, amount):
    return requests.post(f'{BASEURL}/wallet/transact',
                         json={'recipient': recipient, 'amount': amount}).json()

def get_wallet_info():
    return requests.get(f'{BASEURL}/wallet/info').json()

start_blockchain = get_blockchain()
print(f'start blockchain: {start_blockchain}')

recipient = Wallet().address

post_wallet_transaction_a = post_wallet_transaction(recipient, 21)
print(f'\npost wallet transaction a: {post_wallet_transaction_a}')

post_wallet_transaction_b = post_wallet_transaction(recipient, 10)
print(f'\npost wallet transaction b: {post_wallet_transaction_b}')

time.sleep(2)

mined = get_blockchain_mine()
print(f'\nminedblock: {mined}')

print(f'get wallet info: {get_wallet_info()}')