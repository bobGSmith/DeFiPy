'''AutoUI 

Generate user interface for smart contracts automatically given its address and abi

Script
======
Run as a script with:
  python -m DeFiPy.autoui arg1 arg2 arg3

takes 3 args: 
1. contracts_json : path to contracts file. A json formatted like this:
    [{'name':'contract1','abi':ABI,'address':'0xADDRESS'},{'name': etc.. }]
2. networks_json : path to networks file. A json formatted like this:
    {'network1':RPC1,'network2':RPC2}
3. accounts_txt : path to text file encrypted by PwAES, unencrypted it's a 
    json formatted like this:
    {'account1':PRIVATE_KEY_1,'account2':PRIVATE_KEY_2}

Functions 
=========
* choose_from_list : prompt user to chose item from list, returns index of choice
* get_functions : gets functions from abi and returns dict needed to make the UI 
* fix_args : takes array of input arguments and converts to correc types e.g. array 
    like strings are converted to list, addresses (starting with 0x) are checksummed
    and numeric inputs are converted to int. 
* auto_cli : creates a command line interface for contracts 
* auto_dynamic_cli : creates a interactive (curses) command line interface (not made yet)
* auto_gui : creates a graphical user interface with tkinter (not made yet)

'''

from DeFiPy import attach
import json
import time
import pprint

def choose_from_list (choices,prompt):
    choosing = True 
    print(", ".join([f'{i} {x}' for i,x in enumerate(choices)]))
    while choosing: 
        choice = input(prompt).strip()
        if not choice.isnumeric():
            print("choice must be an integer (e.g. 2)")
        elif int(choice) > len(choices) - 1:
            print(f"choice was out of range, select between 0 and {len(choices) - 1}")
        else: 
            return int(choice)

def get_functions(abi):
    functions = {}
    for x in abi:
        if x["type"] == "function":
            functions[x["name"]] = { 
                "name" : x["name"],
                "inputs" : ",".join([f'{y["name"] if y["name"] != "" else f"arg_{i}"} ({y["type"]})' for i,y in enumerate(x["inputs"])]),
                "outputs" : ",".join([f'{y["name"] if y["name"] != "" else f"arg_{i}"} ({y["type"]})' for i,y in enumerate(x["outputs"])]),
                "payable" : x["stateMutability"] == "payable",
                "stateMutability" : x["stateMutability"],
                "n_args" : len(x["inputs"])
            }
    return functions 

def fix_args(w3,args): 
    fixed = []
    for a in args:
        if isinstance(a,list):
            a_fixed = fix_args(w3,a)
            fixed.append(a_fixed)
        elif a[0:2] == "0x" and len(a) == 42:
            try: 
                a_fixed = w3.to_checksum_address(a)
                fixed.append(a_fixed)
            except: fixed.append(a)
        elif a.isnumeric():
            a_fixed = int(a)
            fixed.append(a_fixed)        
        else: 
            fixed.append(a)  
    return fixed

def auto_ui_cli(w3,contracts_json_path, tx_history = {}):
    '''automatically create command line user interface for EVM smart contract
    
    Args
    ====
    * w3 {Web3 object} : Web3 object connected to network and logged in with signer
    * contracts_json_path {str} : path to json file containing an array formatted like this: 
        [{"name":"contract1","abi":ABI,"address":"0xAdDreSS"},{ etc... ]

    Returns 
    =======
    * tx_history {dict} : A dictionary containing all transactions from the session
      indexed by timestamp.
    '''
    with open(contracts_json_path) as infile: 
        all_contracts = json.load(infile)

    print("Contracts:")
    contract_names = [x["name"] for x in all_contracts]
    contract_info = all_contracts[choose_from_list(contract_names,"Select contract (e.g. 1) > ")].copy()
    contract = attach(w3,contract_info["address"],contract_info["abi"])
    functions = get_functions(contract_info["abi"])
    again = True 
    while again: 
        function_names = list(functions.keys())
        fn = functions[function_names[choose_from_list(function_names,"select function (e.g. 1) > ")]]
        
        print(f"function signature: {fn['name']}({fn['inputs']}) returns({fn['outputs']}) payable: {str(fn['payable'])}")

        value = 0
        if fn["payable"]:
            value = int(input("payable function, enter value (wei) > ").strip())

        if fn["inputs"] != "":
            args_entered = False 
            while not args_entered:
                print('Arg Input: separate args by "," args should be wrapped in double quotes e.g.')
                print('  * example args for fn(uint256, uint256[2]) -> "1000000000000000000",["34562","12351"]')
                args = input('Enter args > ')
                if len(args) != fn["n_args"]:
                    print('incorrect number of args entered, remember to separate by "," args should be wrapped in double quotes e.g.')
                    print('  * example args for fn(uint256, uint256[2]) -> "1000000000000000000",["34562","12351"]')
                    input("hit return to try again... ")
                else: args_entered = True
        callable = getattr(contract.functions, fn["name"])
        
        # confirm correct parameters entered
        print_gasprice = f',gasprice: {w3.eth.gas_price}' if fn["payable"] else "" 
        print_tx_data = f"{{'value':{value}{print_gasprice}}}"
        print(f"calling function: {fn['name']}({','.join(args) if fn['inputs'] != '' else ''}){print_tx_data}")
        proceed = input("proceed (y/n) > ").strip().lower() in ["y","yes"]
        
        if proceed: 
            t = int(time.time()) 
            try:
                if fn["stateMutability"] == "view":
                    if fn["inputs"] != "":
                        args = json.loads(f"[{args}]")
                        args = fix_args(w3,args)
                        print(args)
                        tx_history[t] = callable(*args).call() 
                    else: 
                        tx_history[t] = callable().call()
                else: 
                    if fn["inputs"] != "":
                        args = json.loads(f"[{args}]")
                        args = fix_args(w3,args)
                        print(args)
                        tx_history[t] = callable(*args).transact({"value":value,"gasPrice":w3.eth.gas_price})
                    else:
                        tx_history[t] = callable().transact({"value":value,"gasPrice":w3.eth.gas_price})
                print("Transaction executed at ",t)
                pprint.pprint(tx_history[t])
            except Exception as e: 
                print("Error")
                print(e)
        again = input("call another function (y/n) > ").strip().lower() in ["y","yes"]             
    return tx_history



if __name__ == "__main__":
    from DeFiPy import login
    import sys 

    if len(sys.argv) != 4 or sys.argv[1].lower in ["-h","--h","-help","--help"]:
        print(__doc__)
        input("hit return to exit .. ")
        exit() 

    contracts_json_path = sys.argv[1]
    session_info = login(sys.argv[2],sys.argv[3])  

    w3 = session_info["w3"]
    account = session_info["account"]
   
    tx_history = {} 

    new_contract = True 
    while new_contract:
        tx_history = auto_ui_cli(w3,contracts_json_path,tx_history)
        new_contract = input("Interact with another contract (y/n) > ").lower() in ["y","yes"]

    save_tx_history = input("Save session tx history (y/n) > ").lower() in ["y","yes"]
    if save_tx_history:
        save_tx_path = input("enter path to save tx history (./tx_history.json) > ")
        with open(save_tx_path,"w") as outfile: 
            json.dump(tx_history,outfile)
   