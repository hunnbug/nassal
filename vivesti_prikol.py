from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import abi, contract_adress

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
names = w3.eth.accounts
for item in names:
    balance = w3.from_wei(w3.eth.get_balance(item), 'ether')
    print(item, ": баланс: ", balance)