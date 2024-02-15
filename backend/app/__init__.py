from flask import Flask, jsonify
import os
import random
import requests

from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub

app = Flask(__name__)
blockchain = Blockchain()
pubsub = PubSub(blockchain)

@app.route('/')
def route_default():
    return 'Blockchain entry point'

@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.__repr__())

@app.route('/blockchain/mine')
def route_blockchain_mine():
    transaction_data = 'stubbed_transcation_data'

    blockchain.add_block(transaction_data)
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    return jsonify(block.to_json())

ROOT_PORT = 5000
PORT = ROOT_PORT

if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001, 6000)
    result = requests.get(f'http://localhost:{ROOT_PORT}/blockchain')
    result_blockchain = Blockchain.from_json(result.json())

    try:
        blockchain.replace_chain(result_blockchain.chain)
        print('\n -- Successfully synchronised the local chain')
    except Exception as e:
        print(f'\n -- Error synchronising: {e}')
app.run(port=PORT)
