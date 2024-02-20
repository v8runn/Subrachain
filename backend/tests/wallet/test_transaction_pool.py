from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet

def test_set_transaction():
    transcation_pool = TransactionPool()
    transaction = Transaction(Wallet(), 'recipient', 1)
    transcation_pool.set_transaction(transaction)

    assert transcation_pool.transaction_map[transaction.id] == transaction