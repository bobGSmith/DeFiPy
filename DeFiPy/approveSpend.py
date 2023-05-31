def approveSpend(token,amount,spender,verbose = True, POA = False):
    if POA: tx_data = {"gasPrice":50000000000}
    else: tx_data = {}
    try:
        tx = token.functions.approve(spender,amount).transact(tx_data)
        if verbose:
            print(f"success: approved spend {amount} of {token.address} by {spender}")
        return True
    except Exception as e:
        if verbose:
            print(f"fail: {str(e)}")        
        return False
    
def multiApprove(tokens,spenders,amount= 2**(256-1),verbose=True,halt_if_fail=True,POA=False):
    """Approve multiple spenders of multiple tokens

    Args:
        tokens (list): list of web3 ERC20 token contracts
        spenders (list): list of objects with an address attribute returning ethereum address
        amount (int, optional): amount (wei) to approve. Defaults to 2**(256-1).
        verbose (bool, optional): if true prints status info. Defaults to True.
        halt_if_fail (bool, optional): if True terminates approvals if one fails. Defaults to True.

    Returns:
        (list): List of bools corresponding to approvals, True if success
    """
    did_approve = []
    for i in range(len(spenders)):
        for j in range(len(tokens)): 
            approved = approveSpend(tokens[j],amount,spenders[i].address,verbose,POA)
            did_approve.append(approved)
            if not approved and halt_if_fail: return False 
    return did_approve
            