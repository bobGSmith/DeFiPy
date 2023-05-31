def getReservesUni (router,tokenA,tokenB,A_name,B_name):
    return {
        A_name: tokenA.functions.balanceOf(router.address).call(),
        B_name: tokenB.functions.balanceOf(router.address).call()
    }

def getReservesSolidly (router,tokenA,tokenB,A_name,B_name):
    res = router.functions.getReserves(tokenA.address,tokenB.address,False).call()
    return {
        A_name: res[0],
        B_name: res[1]
    }