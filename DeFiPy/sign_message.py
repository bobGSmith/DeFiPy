'''DeFiPy - sign_message

Module 
======

Can import sign_message function which can sign messages with a given private key.


Script
======

Can be ran as script and takes two args: 
* path {str} : path to AES encrypted private key json
* message {str} : the message to be signed 
'''

from web3.auto import w3
from eth_account.messages import encode_defunct

def sign_message(msg,private_key):
    msg = encode_defunct(msg)
    return w3.eth.account.sign_message(msg,private_key)

if __name__ == '__main__':
    from DeFiPy import aes_load_wallets
    import sys 

    if len(sys.argv) == 1:
        print(__doc__)
        exit()
    
    print("DeFiPy - sign_message")
    wallets = aes_load_wallets(sys.argv[1])
    account = input("select private key to use > ")

    print(sign_message(bytes(sys.argv[2],"utf-8"),wallets[account]))

