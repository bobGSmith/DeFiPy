'''Generate ABI json from hardhat artifacts directory

Functions 
=========
genAbi : creates dict of ABIs from hardhat artifacts dir

Args
====
inPath {string} : path to hardhat artifacts/contracts dir
outPath {string} : path to .json to save abis 
'''

import os
import json
import sys


def genAbi (path) : 
    abis = {}
    for f in os.listdir(path):
        if f[-4:].lower() == '.sol':
            if len(os.listdir(f'{path}/{f}')) > 0:
                name = f.replace(".sol","")
                jsonPath = f'{path}/{f}/{name}.json'
                abis[name] = (json.load(open(jsonPath)))["abi"]
        else:
            subAbis = genAbi(f'{path}/{f}')
            for k in subAbis.keys():
                abis[k] = subAbis[k]
    return abis
    

if __name__ == '__main__':
    if len(sys.argv) == 3:
        abis = genAbi(sys.argv[1])
        json.dump(abis, open(sys.argv[2], "w"))
    else: 
        print("genAbis expects two arguments")
        print("1. path_to_hardhat_artifact_dir")
        print("2. path_to_output_json")
        

