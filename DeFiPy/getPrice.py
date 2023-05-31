def getUniV2Price(w3,pair,priceOf,denom,inWei=False):
    res_priceOf = priceOf.functions.balanceOf(pair.address).call() 
    res_denom = denom.functions.balanceOf(pair.address).call() 
    decimals_priceOf = priceOf.functions.decimals().call()
    decimals_denom = denom.functions.decimals().call()
    return getPrice(res_priceOf,res_denom,decimals_priceOf,decimals_denom,inWei)
    
def getSolidlyVarPrice(w3,router,priceOf,denom,inWei=False):
    res = router.functions.getReserves(priceOf.address,denom.address,False).call()
    decimals_priceOf = priceOf.functions.decimals().call()
    decimals_denom = denom.functions.decimals().call()
    return getPrice(res[0],res[1],decimals_priceOf,decimals_denom,inWei)

def getPrice (
    res_priceOf,
    res_denom,
    decimals_priceOf,
    decimals_denom,
    inWei=False):
    res_priceOf = res_priceOf * (10**(18-decimals_priceOf))
    res_denom = res_denom * (10**(18-decimals_denom))
    if inWei:
        return int((res_denom/res_priceOf)  * (10**(decimals_denom)))
    else: 
        return res_denom/res_priceOf
    