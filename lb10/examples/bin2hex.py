#!/usr/bin/env python

def char2bin(s=''):
    return [bin(ord(x))[2:].zfill(8) for x in s]

def bin2char(b=None):
    return ''.join([chr(int(x, 2)) for x in b])

def bin2hex(binary_str):
    return hex(int(binary_str, 2))


if __name__ == '__main__':
    print(bin2hex("10000001"))
    print(char2bin("hello world!"))
