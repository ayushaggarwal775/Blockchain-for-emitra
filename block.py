from hashlib import sha256
import json
import time
from flask import Flask, request
import requests



class Block:
    def __init__(self, index, transactions, timestamp,previous_hash):
        self.index = []
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash


def compute_block(self):
    return sha256(bl.encode()).hexdigest()


class Blockchain:

    def __init__(self):
        self.unconfirmed_Tran = []
        self.chain = []
        self.start_block()

    def start_block(self):
        bl = Block(0,[],time.time(),'0')
        self.chain.append(bl)

    def last(self):
            return self.chain[-1]

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and block_hash == block.compute_hash())


#interface

app =  Flask(__name__)

# the node's copy of blockchain
blockchain = Blockchain()


@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    required_fields = ["author", "content"]

    for field in required_fields:
        if not tx_data.get(field):
            return "Invlaid transaction data", 404

    tx_data["timestamp"] = time.time()

    blockchain.add_new_transaction(tx_data)

    return "Success", 201

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})



@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
    result = blockchain.mine()
    if not result:
        return "No transactions to mine"
    return "Block #{} is mined.".format(result)


# endpoint to query unconfirmed transactions
@app.route('/pending_tx')
def get_pending_tx():
    return json.dumps(blockchain.unconfirmed_transactions)

@app.route("/")
def index():
    return ' '

#app.run(debug=True, port=8000)
if __name__ == '__main__':
    app.run()
