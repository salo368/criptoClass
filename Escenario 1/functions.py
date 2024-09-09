from Crypto.Random import get_random_bytes

def generateKey(bytes_num):
    key = get_random_bytes(bytes_num)
    return key