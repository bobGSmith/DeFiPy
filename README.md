# DeFiPy

Library for interacting with EVM DeFi using web3 py. Includes things for trading on uniswapv2routers, using ERC20 contracts, WETH, calculating price impacts, generating wallets, handling hot wallet private keys with AES encryption. 

## Install 

run: 
```
pip install git+https://github.com/bobGSmith/DeFiPy@master
```

## To Do 
This is a work in progress.. 

* `transact.py` - should maybe improve / test this. not sure how useful it is.  
* `autoUi.py` - need to make this, accepts address and abi for a contract and creates a interface for it (CLI, possibly tkinter too)

## Scripts 
### Auto UI 
generates a user interface for smart contracts automatically from abi and address, run with the following: 

```
python -m DeFiPy.auto_gui arg1 arg2 arg3
```

where the 3 args are: 
1. contracts_json : path to contracts file. A json formatted like this:
    [{'name':'contract1','abi':ABI,'address':'0xADDRESS'},{'name': etc.. }]
2. networks_json : path to networks file. A json formatted like this:
    {'network1':RPC1,'network2':RPC2}
3. accounts_txt : path to text file encrypted by PwAES, unencrypted it's a 
    json formatted like this:
    {'account1':PRIVATE_KEY_1,'account2':PRIVATE_KEY_2}


### Chart 
plots price chart of token in terminal

It takes 3 args, Token, Denominator, n_days, for example: 

```
python3 -m DeFiPy.chart ethereum usd 10
```

