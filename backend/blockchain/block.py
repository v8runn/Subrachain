import time

from backend.util.crypto_hash import crypto_hash
from backend.util.hex_to_binary import hex_to_binary
from backend.config import MINE_RATE
from backend.util.poh import compute_vdf, verify_vdf

GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'genesis_last_hash',
    'hash': 'genesis_hash',
    'data': [],
    'difficulty': 8,
    'nonce': 'genesis_nonce',
    'poh_record': 0,
    'vdf_output': 0,
    'vdf_params': ['genesis_pi', 'genesis_g', 'genesis_N']
}

class Block:
    def __init__(self, timestamp, last_hash, hash, data, difficulty, nonce, poh_record, vdf_output, vdf_params):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce
        self.poh_record = poh_record
        self.vdf_output = vdf_output
        self.vdf_params = vdf_params

    def __repr__(self):
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'last_hash: {self.last_hash}, '
            f'hash: {self.hash}, '
            f'data: {self.data}, '
            f'difficulty: {self.difficulty}, '
            f'nonce: {self.nonce},)'
            f'poh_record: {self.poh_record},)'
            f'vdf_output {self.vdf_output},)'
            f'vdf_params: {self.vdf_params})'
        )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_json(self):
        return self.__dict__

    @staticmethod
    def mine_block(last_block, data):
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = Block.adjust_difficulty(last_block, timestamp)
        nonce = 0
        poh_record = last_block.poh_record + 1

        vdf_input = f'{last_hash}{timestamp}{poh_record}'
        vdf_output, vdf_params = compute_vdf(vdf_input, 10)
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce, poh_record, vdf_output, vdf_params)

        while hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce, poh_record, vdf_output, vdf_params)

        return Block(timestamp, last_hash, hash, data, difficulty, nonce, poh_record, vdf_output, vdf_params)

    @staticmethod
    def genesis():
        """
        Generate the genesis block.
        """
        return Block(**GENESIS_DATA)

    @staticmethod
    def from_json(block_json):
        return Block(**block_json)

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        if (new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1

        if (last_block.difficulty - 1) > 0:
            return last_block.difficulty - 1

        return 1

    @staticmethod
    def is_valid_block(last_block, block):
        if block.last_hash != last_block.hash:
            raise Exception('The block last hash must be correct')

        if hex_to_binary(block.hash)[0:block.difficulty] != '0' * block.difficulty:
            raise Exception('The POW requirement was not met')

        if abs(last_block.difficulty - block.difficulty) > 1:
            raise Exception('The block difficulty is not adjusted by 1')
        
        if (block.poh_record - last_block.poh_record) > 1:
            raise Exception('PoH record is incorrect')
        
        if not verify_vdf(block.vdf_output, block.vdf_params, 10):
            raise Exception('Invalid VDF output')

        reconstructed_hash = crypto_hash(
            block.timestamp,
            block.last_hash,
            block.data,
            block.difficulty,
            block.nonce,
            block.poh_record,
            block.vdf_output,
            block.vdf_params
        )

        if block.hash != reconstructed_hash:
            raise Exception('The block hash must be correct')

def main():
    genesis_block = Block.genesis()
    bad_block = Block.mine_block(genesis_block, 'badblock')
    bad_block.last_hash = 'jdjdjdj'

    try:
        Block.is_valid_block(genesis_block, bad_block)
    except Exception as e:
        print(f'is_valid_block: {e}')

if __name__ == '__main__':
    main()

    
