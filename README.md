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
generates a user interface for smart contracts automatically from abi and address 

### Chart 
plots price chart of token in terminal
