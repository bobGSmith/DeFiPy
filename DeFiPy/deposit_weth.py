def deposit_weth (WETH,amountWei,verbose=True,POA=False):
    if POA: tx_data = {"value":amountWei,"gasPrice":50000000000} 
    else: tx_data = {"value":amountWei} 
    try :
        tx = WETH.functions.deposit().transact(tx_data)
        if verbose: print("deposit WETH success: ",tx.hex()) # 
        return (True,tx)
    except Exception as e: 
        if verbose: print("deposit WETH fail: ", str(e))
        return (False,e) 