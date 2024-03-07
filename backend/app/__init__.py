import os
import requests
import random
from Crypto.Cipher import AES  
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import json
import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from backend.blockchain.blockchain import Blockchain
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool
from backend.pubsub import PubSub


app = Flask(__name__)
CORS(app, resources={ r'/*': {'origins': 'http://localhost:3000'}})
blockchain = None
wallet = None
transaction_pool = None
pubsub = None

def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    return ct_bytes

def decrypt_data(encrypted_data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    pt = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return pt.decode()

def load_data():
    blockchain_file_name = 'blockchain_data' + wallet_address + '.bin'
    transaction_pool_file_name = 'transaction_pool_data' + wallet_address + '.bin'
    key_file_name = 'key' + wallet_address + '.bin'
    try:
        with open(blockchain_file_name, 'rb') as file:
            encrypted_blockchain = file.read()
        with open(transaction_pool_file_name, 'rb') as file:
            encrypted_transaction_pool = file.read()
        
        with open(key_file_name, 'rb') as file:
            key = file.read()

        blockchain_data = decrypt_data(encrypted_blockchain, key)
        transaction_pool_data = decrypt_data(encrypted_transaction_pool, key)

        blockchain = Blockchain.from_json(json.loads(blockchain_data))
        transaction_pool = json.loads(transaction_pool_data)

        return blockchain, transaction_pool
    except FileNotFoundError:
        return Blockchain(), TransactionPool()

def save_data(blockchain, transaction_pool):
    blockchain_file_name = 'blockchain_data' + wallet_address + '.bin'
    transaction_pool_file_name = 'transaction_pool_data' + wallet_address + '.bin'
    key_file_name = 'key' + wallet_address + '.bin'

    key = get_random_bytes(16)
    with open(key_file_name, 'wb') as file:
        file.write(key)

    encrypted_blockchain = encrypt_data(json.dumps(blockchain.to_json()), key)
    encrypted_transaction_pool = encrypt_data(json.dumps(transaction_pool.transaction_data()), key)

    with open(blockchain_file_name, 'wb') as file:
        file.write(encrypted_blockchain)
    with open(transaction_pool_file_name, 'wb') as file:
        file.write(encrypted_transaction_pool)

def initialize_wallet_with_address(address):
    new_wallet = Wallet(blockchain)
    new_wallet.address = address
    return new_wallet

@app.route('/')
def route_default():
    return 'Blockchain backend'

@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())

@app.route('/blockchain/range')
def route_blockchain_range():
    start = int(request.args.get('start'))
    end = int(request.args.get('end'))

    return jsonify(blockchain.to_json()[::-1][start:end])

@app.route('/blockchain/length')
def route_blockchain_length():
    return jsonify(len(blockchain.chain))

@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = transaction_pool.transaction_data()
    transaction_data.append(Transaction.reward_transaction(wallet).to_json())
    blockchain.add_block(transaction_data)

    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    transaction_pool.clear_blockchain_transactions(blockchain)
    save_data(blockchain, transaction_pool)

    return jsonify(block.to_json())

@app.route('/wallet/transact', methods=['POST'])
def route_wallet_transact():
    transaction_data = request.get_json()
    transaction = transaction_pool.existing_transaction(wallet.address)

    if transaction:
        transaction.update(
            wallet,
            transaction_data['recipient'],
            transaction_data['amount']
        )
    else:
        transaction = Transaction(
            wallet,
            transaction_data['recipient'],
            transaction_data['amount']
        )

    pubsub.broadcast_transaction(transaction)
    transaction_pool.set_transaction(transaction)
    save_data(blockchain, transaction_pool)

    return jsonify(transaction.to_json())

@app.route('/wallet/info')
def route_wallet_info():
    return jsonify({'address': wallet.address, 'balance': wallet.balance})

@app.route('/known-addresses')
def route_known_addresses():
    known_addresses = set()

    for block in blockchain.chain:
        for transaction in block.data:
            known_addresses.update(transaction['output'].keys())

    return jsonify(list(known_addresses))

@app.route('/transactions')
def route_transactions():
    return jsonify(transaction_pool.transaction_data())

def initialize():
    global wallet, blockchain, transaction_pool, pubsub, wallet_address
    blockchain = Blockchain()
    transaction_pool = TransactionPool()
    pubsub = PubSub(blockchain, transaction_pool)

    wallet_address = os.environ.get('WALLET_ADDRESS')
    if wallet_address:
        wallet = initialize_wallet_with_address(wallet_address)
    else:
        wallet = Wallet(blockchain)
        wallet_address = wallet.get_address()
        
    try:
        if not load_data():
            print("No existing data found, starting new node")
            pubsub.broadcast_state_request()
            save_data(blockchain, transaction_pool)
        else:
            pubsub.broadcast_state_request()
            save_data(blockchain, transaction_pool)
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        pass

PORT = 5000

if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001, 6000) 

if os.environ.get('SEED_DATA') == 'True':
    for i in range(10):
        blockchain.add_block([
            Transaction(Wallet(), Wallet().address, random.randint(2, 50)).to_json(),
            Transaction(Wallet(), Wallet().address, random.randint(2, 50)).to_json()
        ])

    for i in range(3):
        transaction_pool.set_transaction(
            Transaction(Wallet(), Wallet().address, random.randint(2, 50))
        )

initialize()
app.run(port=PORT)
