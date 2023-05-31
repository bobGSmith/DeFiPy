import time

def swapTokensForTokens(account,router,tokenA,tokenB,amountIn,minRecieve,isSolidly=False,verbose=True,customGasPrice=None):
    if not customGasPrice == None: 
        tx_data= {"gasPrice":customGasPrice}
    else: tx_data = {} 
    if isSolidly:
        path = [(tokenA.address,tokenB.address,False)]
    else:     
        path = [tokenA.address,tokenB.address]
    try: 
        tx = router.functions.swapExactTokensForTokens(
            int(amountIn), 
            int(minRecieve),
            path,
            account.address,
            int(time.time()+1000)
        ).transact(tx_data)
        if verbose: print(f"successfull swap: {tx.hex()}")
        return (True,tx)
    except Exception as e:
        if verbose: print(f"fail: {str(e)}")
        return (False,e)
    


