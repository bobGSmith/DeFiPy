import sys 
import json

def abiToString (path,outpath):
    with open (path, "r") as infile: 
        data = infile.read()
    abi = data.replace("\n","").replace(" ","")
    with open(outpath, "w")as outfile: 
        outfile.write(abi)

if __name__ == '__main__':
    
    path = sys.argv[1]
    outpath = sys.argv[2]

    abiToString(path,outpath)