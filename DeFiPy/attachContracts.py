import json 

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