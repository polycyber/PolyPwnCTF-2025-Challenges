# This little decryption gonna cost us 52 years
## Write-up FR

Ce challenge est basé sur la vérification de signature. L'objectif est de signer et vérifier des messages avec une clé RSA tout en respectant certaines restrictions. Une signature RSA est utilisée pour authentifier un message et garantir qu'il n'a pas été altéré. Ici, le serveur empêche les utilisateurs de signer `ADMIN_TOKEN`, donc le défi consiste à trouver un moyen de forger une signature valide pour ce message sans la clé privée. Toutes les explications concernant la vérification de signatures RSA sont ici : `https://cryptobook.nakov.com/digital-signatures/rsa-signatures`.

On peut résoudre ce challenge avec python :

```python
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
```

## Write-up EN

This challenge is based on signature verification. The aim is to sign and verify messages with an RSA key while complying with certain restrictions. An RSA signature is used to authenticate a message and guarantee that it has not been altered. Here, the server prevents users from signing `ADMIN_TOKEN`, so the challenge is to find a way to forge a valid signature for this message without the private key. Full explanations of RSA signature verification can be found here: `https://cryptobook.nakov.com/digital-signatures/rsa-signatures`.

## Flag

`polycyber{S1gn4tur3_1s_1mp0rt4nt_bu7_n0t_4lw4ys_s3cur3}`
