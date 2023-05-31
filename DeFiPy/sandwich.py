'''Sandwich

functions for executing sandwich attacks, still needs work.. 
'''

import asyncio
from .swapTokensForTokens import swapTokensForTokens

def binarySearch (left, right, calculateF, passConditionF, tolerance = 0.01):
    if right - left > tolerance * ((right + left) // 2):
        mid = right + left // 2
        out = calculateF(mid)
        if passConditionF(out):
            return binarySearch(mid,right,calculateF,passConditionF,tolerance)
        return binarySearch(left, mid, calculateF, passConditionF, tolerance)
    ret = (right + left) // 2
    if ret < 0:
        return 0
    return ret 

def getUniV2DataGivenIn (aIn, reserveA, reserveB) :
    aInWithFee = aIn * 997
    numerator = aInWithFee * reserveB
    denominator = aInWithFee + (reserveA * 1000)
    bOut = numerator // denominator 
    newReserveB = reserveB - bOut 
    if newReserveB < 0 or newReserveB > reserveB:
        newReserveB = 1
    newReserveA = reserveA + aIn
    if newReserveA < reserveA: 
        newReserveA = 2**(256-1)
    return {
        "amountOut": bOut, 
        "newReserveA":newReserveA, 
        "newReserveB":newReserveB
    }



def calcSandwichState (optimalSandwichWethIn, userWethIn, userMinRecv, reserveWeth, reserveToken):
    frontrunState = getUniV2DataGivenIn(optimalSandwichWethIn,reserveWeth,reserveToken)
    victimState = getUniV2DataGivenIn(userWethIn,frontrunState["newReserveA"],frontrunState["newReserveB"])
    backrunState = getUniV2DataGivenIn(frontrunState["amountOut"],victimState["newReserveB"],victimState["newReserveA"])
    if victimState["amountOut"] < userMinRecv:
        return None 
    return {
        "revenue":backrunState["amountOut"] - optimalSandwichWethIn,
        "optimalSandwichWethIn": optimalSandwichWethIn,
        "userAmountIn":userWethIn,
        "userMinRecv":userMinRecv,
        "reserveState":{"reserveWeth":reserveWeth, "reserveToken":reserveToken},
        "frontrun":frontrunState,
        "victim":victimState,
        "backrun":backrunState
    }

def calcSandwichOptimalIn(userAmountIn, userMinRecvToken, reserveWeth, reserveToken):
    def calcF (amountIn): 
        frontrunState = getUniV2DataGivenIn(amountIn, reserveWeth, reserveToken)
        victimState = getUniV2DataGivenIn(userAmountIn, frontrunState["newReserveA"], frontrunState["newReserveB"])
        return victimState["amountOut"]
    def passF (amountOut): 
        return amountOut >= userMinRecvToken
    # upper bound should probs be eth balance, lower could be calculated some other way
    lowerBound = 0 
    upperBound = 10 * (10**18)
    optimalWethIn = binarySearch(lowerBound, upperBound, calcF, passF)
    return optimalWethIn        



async def doubleTx (
    account1,router1,tokenA1,tokenB1,amountIn1,minRecieve1,isSolidly1,verbose,frontrunGas,
    account2,router2,tokenA2,tokenB2,amountIn2,minRecieve2,isSolidly2,backrunGas
) : 
    reciepts = asyncio.run(
        await asyncio.gather(
        swapTokensForTokens(account1,router1,tokenA1,tokenB1,amountIn1,minRecieve1,isSolidly1,verbose,frontrunGas),
        swapTokensForTokens(account2,router2,tokenA2,tokenB2,amountIn2,minRecieve2,isSolidly2,verbose,backrunGas)
    )    
    )
    return reciepts 