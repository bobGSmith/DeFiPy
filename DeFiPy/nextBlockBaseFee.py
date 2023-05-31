import random
def nextBlockBaseFee(w3,verbose = True):
    block  = w3.eth.get_block("latest") 
    if verbose: print("cur base fee: ", block["baseFeePerGas"])
    baseFee = block["baseFeePerGas"]
    gasUsed = block["gasUsed"]
    targetGasUsed = block["gasLimit"] // 2
    delta = gasUsed - targetGasUsed
    newBaseFee = baseFee + (((baseFee * delta)/targetGasUsed)//8)
    rand = random.randint(0,9)
    return int(newBaseFee + rand) 
        
if __name__ == '__main__':
    from w3tools import * 
    wallets = aes_load_wallets("./accounts.txt")
    account = input("enter selected wallet name from above > ")
    #w3,account = connect_with_local_account(wallets[account],rpc_url="	https://1rpc.io/eth") #"https://rpc.ankr.com/fantom/")
    w3,account = connect_with_local_account(wallets[account],rpc_url="https://rpc.ankr.com/fantom/")
    print(nextBlockBaseFee(w3))
    