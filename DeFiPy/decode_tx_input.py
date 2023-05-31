import time

def decode_tx_input (transaction,Contract,verbose=True):
    decode = Contract.decode_function_input(transaction["input"])
    if verbose: 
        function_input = []
        for key in decode[1].keys():
            function_input.append( f"{key} - {decode[1][key]}")               
        function_input = "\n  * ".join(function_input)
        print(f'Transaction {int(time.time())}:\nhash {transaction["hash"].hex()}\nto {transaction["to"]}\nfrom {transaction["from"]}\ngas {transaction["gas"]}\ngas price {transaction["gasPrice"]}\nvalue {transaction["value"]}\nfunction {decode[0].fn_name}\n  * {function_input}')
    return decode