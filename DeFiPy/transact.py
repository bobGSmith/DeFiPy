from eth_account import Account

def buildTxData (w3,caller,value,optional_params = {}) :
    if not value in [0,"0",False]:
        tx_data ={
            "chainId":w3.eth.chainId,
            "from":caller,
            "nonce":w3.eth.get_transaction_count(caller),
            "value":value
        } 
    else:
        tx_data = {
            "chainId":w3.eth.chainId,
            "from":caller,
            "nonce":w3.eth.get_transaction_count(caller)
        } 
    for k in optional_params.keys(): 
        tx_data[k] = optional_params[k]
    return tx_data

def transact (w3,wallet,func,value,verbose=True):
    tx_data = func.buildTransaction(buildTxData(w3,wallet,value))
    tx_reciept = sendTransaction(w3,wallet,tx_data,verbose=verbose)
    return tx_reciept

def sendTransaction (w3,wallet,tx_reciept,verbose=True): 
    signed_tx = w3.eth.account.sign_transaction(tx_reciept,private_key=wallet)
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx = w3.eth.wait_for_transaction_receipt(send_tx)
    if verbose: 
        print(f"tx: {tx.transactionHash.hex()}")
    return tx
    
