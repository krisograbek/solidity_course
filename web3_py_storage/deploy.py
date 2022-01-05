import json
import os
from solcx import compile_standard
from solcx import install_solc
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as f:
    simple_storage_file = f.read()

# compile solidity
install_solc("0.8.0")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.0",
)

with open("compiled_code.json", "w") as f:
    json.dump(compiled_sol, f)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# print(abi)

# connecting to ganache
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/d88668b8da4d444cbcc64866c7461307")
)
chain_id = 4
my_address = "0x55595eD1bb53a2C54C4C6818773ace899A971959"
private_key = os.getenv("PRIVATE_KEY")

# create the contract in Python
print("Deploying contract")
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# print(SimpleStorage)

# get nonce
nonce = w3.eth.getTransactionCount(my_address)

# We need 3 steps
# 1. Build a Transaction
# 2. Sign a Transaction
# 3. Send a Transaction

transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# sent the signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed! ")

# working with the conract, we need
# Contract address
# Contract ABI

print("Updating contract ")
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# get the initial favNumber value (from solidity)
print("Initial favNumber")
print(simple_storage.functions.retrieve().call())

# try assign a new value to favNumber with call
# print(simple_storage.functions.store(15).call())
# # the favNumber value didn't change
# print(simple_storage.functions.retrieve().call())

# make a transaction that changes the favNumber

store_transaction = simple_storage.functions.store(20).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
# sign transaction
signed_store_tx = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

# send the signed transaction
store_tx_hash = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
store_tx_receipt = w3.eth.wait_for_transaction_receipt(store_tx_hash)

print("New favNumber")
print(simple_storage.functions.retrieve().call())
