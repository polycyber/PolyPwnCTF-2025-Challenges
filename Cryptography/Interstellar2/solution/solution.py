from pwn import *
import json, random
from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse
from sympy import gcd

# Configuration du serveur
host = 'localhost'
port = 1333
conn = remote(host, port)

print(conn.recv().decode('utf-8'))
conn.send(json.dumps({"option": 'get_pubkey'}).encode())
data = json.loads(conn.recv().decode('utf-8'))

N = int(data['N'],16)
e = int(data['e'],16)

r = random.randint(2,N)
while gcd(r,e) != 1:
    r = random.randint(2,N)
    
ADMIN_TOKEN = b"Thorne=True"
msg = long_to_bytes((bytes_to_long(ADMIN_TOKEN)*r**e)%N)

conn.send(json.dumps({"option": 'sign', 'msg': msg.hex()}).encode())
msg_sign = int(json.loads(conn.recv().decode('utf-8'))["signature"],16)

sign = long_to_bytes((msg_sign*inverse(r,N))%N)

conn.send(json.dumps({"option": 'verify', 'msg': ADMIN_TOKEN.hex(), 'signature': sign.hex()}).encode())
print(json.loads(conn.recv().decode('utf-8')))