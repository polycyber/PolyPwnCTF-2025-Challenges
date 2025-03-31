from Crypto.Util.number import bytes_to_long, getPrime
from sympy import *
import random

e = None
while e is None:
    try:
        p = getPrime(1024)
        q = getPrime(1024)
        n = p*q
        born = integer_nthroot(n, 4)[0]//3
        d = random.getrandbits(born.bit_length())
        e = pow(d,-1,(p-1)*(q-1))
    except:
        e = None

message = b"Welcome aboard! Here's my welcome present: polycyber{W13nn3r_15_th1_50lut10n}"
encrypted = pow(bytes_to_long(message), e, n)

print(f'Public key:\n- n = {hex(n)}\n- e = {hex(e)}\nEncrypted message from CASE: {hex(encrypted)}')