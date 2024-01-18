import json 
import requests

def attachContracts(w3,contracts_path,verbose=True):
    '''takes path to .json file containing array of jsons with address, name, abi of contracts'''
    file = open(contracts_path,"r")
    Contracts = json.load(file)
    file.close()
    contracts = {}
    for C in Contracts: 
        contracts[C["name"]] = w3.eth.contract(address=w3.to_checksum_address(C["address"]),abi=C["abi"])
    if verbose: 
        contractsString = '\n  * '.join(list(contracts.keys()))
        print(f"Attached contracts:\n  * {contractsString}")
    return contracts

def attach(w3,address,abi):
    return w3.eth.contract(
        address = w3.to_checksum_address(address),
        abi = abi
    )

def quick_attach (w3, address, block_explorer_url="https://api.etherscan.io/"):
    '''Attach to verified contract, getting abi from blockexplorer api'''
    abi = requests.get(f"{block_explorer_url}api?module=contract&action=getabi&address={address}&format=raw")
    return w3.eth.contract(
        address = w3.to_checksum_address(address),
        abi = abi.json()
    )