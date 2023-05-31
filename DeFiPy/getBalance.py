def getBalance(token,address):
    return token.functions.balanceOf(address).call()