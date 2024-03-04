import time
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-cd8f5f7a-50d1-40b2-b7e6-a096639d058f'
pnconfig.publish_key = 'pub-c-c6badcb8-d05a-4d32-84a1-2b98b21d55dc'

CHANNELS = {
    'TEST': 'TEST',
    'BLOCK': 'BLOCK',
    'TRANSACTION': 'TRANSACTION'
}

class Listener(SubscribeCallback):
    def __init__(self, blockchain, transaction_pool):
        self.blockchain = blockchain
        self.transaction_pool = transaction_pool

    def message(self, pubnub, message_object):
        print(f'\n-- Channel: {message_object.channel} | Message: {message_object.message}')

        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_object.message)
            pot_chain = self.blockchain.chain[:]
            pot_chain.append(block)
            try:
                self.blockchain.replace_chain(pot_chain)
                self.transaction_pool.clear_blockchain_transactions(self.blockchain)
                print('\n--Succesfully replaced chain')
            except Exception as e:
                print(f'\n-- Did not replace chain: {e}')
        elif message_object.channel == CHANNELS['TRANSACTION']:
            transaction = Transaction.from_json(message_object.message)
            self.transaction_pool.set_transaction(transaction)
            print('\n -- Set the new transaction in the transaction pool')

            

class PubSub():
    def __init__(self, blockchain, transcation_pool):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain, transcation_pool))

    def publish(self, channel, message):
        self.pubnub.unsubscribe().channels([channel]).execute()
        self.pubnub.publish().channel(channel).message(message).sync()
        self.pubnub.subscribe().channels([channel]).execute()

    def broadcast_block(self, block):
        self.publish(CHANNELS['BLOCK'], block.to_json())
    
    def broadcast_transaction(self, transaction):
        self.publish(CHANNELS['TRANSACTION'], transaction.to_json())

def main():
    pubsub = PubSub()
    time.sleep(1)
    pubsub.publish(CHANNELS['TEST'], {'testing': 'block'})

if __name__ == '__main__':
    main()



