#!/usr/bin/env python
import hashlib

def sha1(text):
    try:
        # python 2
        hash_object = hashlib.sha1(text)
        return hash_object.hexdigest()
    except:
        # python 3
        hash_object = hashlib.sha1(text.encode())
        return hash_object.hexdigest()



if __name__ == '__main__':
    print(sha1("Hello World"))