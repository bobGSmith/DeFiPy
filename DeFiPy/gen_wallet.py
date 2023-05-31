'''Generate Crypto Wallet

generate crypto wallet private key + public address pair and optionally password based AES_encrypt it
''' 

from eth_account import Account 
import secrets 

def fixPath (path):
    return "/".join(path.split("\\")).replace('"','')


def gen_wallet(): 
    key = f"0x{secrets.token_hex(32)}"
    wallet = {
        "account":Account.from_key(key).address, 
        "key":key
    }
    return wallet

if __name__ == '__main__':
    import sys 
    import json 
    import time
    
    path = f"{fixPath(sys.argv[1])}/wallet_{int(time.time())}.json"
    wallet = gen_wallet()
    with open(path,"w") as outfile: 
        json.dump(wallet,outfile)

    print(f"Wallet {wallet['account']} written to ", path)    
    