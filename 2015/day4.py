import aocd
import hashlib

def find_secret_key_hash(secret_key, required_zeros = 5):
    
    i = 0
    while True:
        
        key = secret_key + str(i)
        md5 = hashlib.md5(key.encode("utf-8")).hexdigest()
        
        if all([char == "0" for char in md5[:required_zeros]]):
            return i
        i += 1
    
if __name__ == "__main__":
    
    secret_key = aocd.get_data(day = 4, year = 2015)
    print(find_secret_key_hash(secret_key))
    print(find_secret_key_hash(secret_key, 6))
    