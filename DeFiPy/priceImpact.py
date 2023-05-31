from .getPrice import getPrice
from .getAmountOut import getAmountOut, getAmountOutSolidlyVol

def simulateTrade(resIn,resOut,amountIn,isSolidly=False) :
    if isSolidly:
        amountOut = getAmountOutSolidlyVol(amountIn,resIn,resOut)
    else: 
        amountOut = getAmountOut(amountIn, resIn, resOut)
    return resIn + amountIn, resOut - amountOut, amountOut

def simulateArb (amountIn,reservesArray,isSolidlyArray):
    '''Get amount out from arb. reservesArray is array of swap path tuples [(in_token, out_token)]'''    
    for i, path in enumerate(reservesArray): 
        _, _, amountIn = simulateTrade(path[0],path[1],amountIn,isSolidlyArray[i])
    return amountIn 
    
def getPostTradePriceOfOut(amountIn,resIn,resOut,decimalsIn,decimalsOut,isSolidly=False):
    simIn, simOut, amountOut = simulateTrade(resIn,resOut,amountIn,isSolidly)
    return getPrice(simOut,simIn,decimalsOut,decimalsIn,inWei=True), simIn, simOut, amountOut
    
def priceImpactSellSize (
    target_price,
    reserveA,
    reserveB,
    decimalsA,
    decimalsB,
    size = 0,
    step_size = 10000000000000000,
    isSolidly = False):
    '''find the sell size of token A needed to push price of token B to target price'''
    price = getPrice(reserveB,reserveA,decimalsB,decimalsA,inWei=True)
    prev_price = price
    prev_size = size
    while price < target_price:
        prev_price = price
        prev_size = size
        size += step_size 
        price, _, _, _ = getPostTradePriceOfOut(size,reserveA,reserveB,decimalsA,decimalsB,isSolidly)
    return prev_size


def convergePrices(
    dex1_resA,
    dex1_resB,
    dex2_resA,
    dex2_resB,
    decimalsA,
    decimalsB,
    dex1_isSolidly,
    dex2_isSolidly,
    size = 0,
    step_size = 100000000000000):
    '''Find amount tokenA to sell on dex 1 then sell tokenB on dex 2 to converge prices'''
    b_price_dex_1 = getPrice(dex1_resB,dex1_resA,decimalsB,decimalsA,inWei=True)
    b_price_dex_2 = getPrice(dex2_resB,dex2_resA,decimalsB,decimalsA,inWei =True)
    prev_b_price_dex_1 = b_price_dex_1
    prev_b_price_dex_2 = b_price_dex_2
    prev_size = size
    while b_price_dex_1 < b_price_dex_2: 
        prev_b_price_dex_1 = b_price_dex_1
        prev_b_price_dex_2 = b_price_dex_2
        prev_size = size
        size += step_size 
        b_price_dex_1, new_dex1_resA, new_dex1_resB, dex1_amountOutB = getPostTradePriceOfOut(size,dex1_resA,dex1_resB,decimalsA,decimalsB,dex1_isSolidly)
        a_price_dex_2, new_dex2_resB, new_dex2_resA, dex2_amountOutA = getPostTradePriceOfOut(dex1_amountOutB,dex2_resB,dex2_resA,decimalsB,decimalsA,dex2_isSolidly)
        b_price_dex_2 = getPrice(new_dex2_resB,new_dex2_resA,decimalsB,decimalsA,inWei=True)
    return prev_size
