from backend.blockchain.block import Block

class Blockchain:
    """
    Implementing a list of blocks
    """

    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'
    
    def replace_chain(self, chain):
        """
        Replace the local chain with the incoming one if these apply:
        - The incoming chain must be longer than the local one
        - The incoming chain is formatted properly.
        """
        if len(chain) <= len(self.chain):
            raise Exception('The incoming chain must be longer so cannot replace')
        
        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f'Cannot replace, the incoming chain is valid: {e}')
        
        self.chain = chain

    def to_json(self):
        return list(map(lambda block: block.to_json(), self.chain))
    
    @staticmethod
    def from_json(chain_json):
        blockchain = Blockchain()
        blockchain.chain = list(map(lambda block_json: Block.from_json(block_json), chain_json))

        return blockchain

    @staticmethod
    def is_valid_chain(chain):
        """
        Validate the incoming chain and enforce the following rules:
        - The chain must start with the genesis block
        - Blocks must be formatted correctly
        """

        if chain[0] != Block.genesis():
            raise Exception('Invalid genesis block')

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_valid_block(last_block, block)


def main():
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')

    print(blockchain)

if __name__ == '__main__':
    main()
