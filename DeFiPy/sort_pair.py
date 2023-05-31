def sort_pair (addressA, addressB, symbolA, symbolB):
    sorted = {} 
    sorted[int(addressA,16)] = symbolA
    sorted[int(addressB,16)] = symbolB 
    sorted_keys = list(sorted.keys())
    sorted_keys.sort()
    return sorted[sorted_keys[0]],sorted[sorted_keys[1]]