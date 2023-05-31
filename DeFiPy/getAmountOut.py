
def getAmountOut(amountIn,reserveIn,reserveOut,fee=997,intify=True):
    amountInFee = amountIn * fee
    numerator = amountInFee * reserveOut
    denominator = (reserveIn * 1000) + amountInFee
    amountOut = numerator/denominator
    if intify: 
        amountOut = int(amountOut)
    return amountOut

from decimal import Decimal 
def getAmountOutDecimal(amountIn,reserveIn,reserveOut,fee=997,intify=False):
    amountIn = Decimal(amountIn)
    reserveIn = Decimal(reserveIn)
    reserveOut = Decimal(reserveOut)
    fee = Decimal(fee)
    return getAmountOut(amountIn,reserveIn,reserveOut,fee,intify=intify)
    

def getAmountOutSolidlyVol(amountIn,reserveIn,reserveOut,fee=2700,intify=True): 
    amountIn -= amountIn *  fee / 1e6
    amountOut = amountIn * reserveOut / (reserveIn + amountIn)
    if intify: 
        amountOut = int(amountOut)
    return amountOut
