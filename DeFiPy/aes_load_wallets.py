from PwAES import decrypt_cyphertext_file, gen_pw_privatekey
import json
import hashlib

def aes_load_wallets (path,verbose=True,get_pw=True,pw="") :
    '''Load wallets from aes encrypted json. if get_pw, the user will
    be prompted to enter their password at the terminal, if False, you can
    pass the password in via the pw arg.
    
    Example wallets file: 

    {
        wallet1: "private_key_for_wallet1"
    }

    '''
    if get_pw: 
        pwpk = gen_pw_privatekey()
    else: 
        pwpk = hashlib.sha256(pw.encode('utf-8')).digest()
    wallets = decrypt_cyphertext_file(path,pwpk)
    wallets = json.loads(wallets)
    if verbose: 
        walletString = '\n  * '.join(list(wallets.keys()))
        print(f"Wallets loaded:\n  * {walletString}")
    return wallets
    

if __name__ == '__main__':
    import sys
    aes_load_wallets(sys.argv[1])