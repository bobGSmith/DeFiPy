from web3 import Web3
from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3.middleware import construct_sign_and_send_raw_middleware, geth_poa_middleware

def connect(rpc_url="http://127.0.0.1:8545/", verbose = True, wss_or_http = "http"):
    if wss_or_http == "http":
        w3 = Web3(Web3.HTTPProvider(rpc_url))
    elif wss_or_http == "wss": 
        w3 = Web3(Web3.WebsocketProvider(rpc_url))
    if verbose: 
        if w3.is_connected():
            print(f"connected via {wss_or_http}")
        else:
            print("connection failed")
    return w3 

def connect_with_local_account (
    private_key,
    rpc_url="http://127.0.0.1:8545/", 
    POA = False,
    verbose = True,
    wss_or_http = "http"):
    w3 = connect(rpc_url,verbose,wss_or_http)
    account: LocalAccount = Account.from_key(private_key)
    if POA: w3.middleware_onion.inject(geth_poa_middleware,layer=0)
    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))
    w3.eth.default_account = account.address
    if verbose: print(f"Account: {account.address}")
    return w3,account
    
    