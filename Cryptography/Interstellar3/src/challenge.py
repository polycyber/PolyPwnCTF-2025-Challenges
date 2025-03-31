from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes
import random
from really_secret_message import message

def generate_rsa_KIPP_key(bits: int = 2048) -> tuple[int,int]:
    # Génère une clé RSA
    key = RSA.generate(bits, e=17)
    n = key.n
    e = key.e
    return n, e

def generate_random_polynomial(n: int, degree: int) -> list[int]:
    # Génère un polynôme aléatoire de degré donné avec des coefficients dans Z/nZ
    coefficients = [random.randint(2, n-1) for _ in range(degree + 1)]
    return coefficients

def encryption(message: bytes, p: list[int], n: int, e: int) -> bytes:
    m = bytes_to_long(message)
    pm = sum(coef * m**i for i, coef in enumerate(p))
    return long_to_bytes(pow(pm,e,n))

def send_encrypted_message(n: int, e: int, k: int, message: bytes, to: str) -> str:
    p = generate_random_polynomial(n, k)
    c = encryption(message, p, n, e)
    print(f'To {to}:')
    print(f"RSA public key :\n- n = {hex(n)}\n- e = {hex(e)}")
    print(f"Polynomial of degree {k} in Z/nZ : {[hex(a) for a in p]}")
    print(f'Encryption : {c.hex()}\n')
    return p, c

# Paramètres
k1 = 5
k2 = 5

# Génération de la clé RSA
n, e = generate_rsa_KIPP_key()

# Chiffrement
p1, c1 = send_encrypted_message(n, e, k1, message, 'TARS')
p2, c2 = send_encrypted_message(n, e, k2, message, 'KIPP')