from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.PublicKey import RSA
import signal, json

FLAG = 'polycyber{????????????????????????????????????????????}'
ADMIN_TOKEN = b"Thorne=GOAT"

class Challenge():
    def __init__(self):
        myKey = RSA.generate(2048)
        self.N = myKey.n
        self.E = myKey.e
        self.D = myKey.d
        
    def challenge(self, your_input):
        if 'option' not in your_input:
            return {"error": "You should provide an option among 'get_pubkey', 'sign' or 'verify'"}
        
        elif your_input['option'] == 'get_pubkey':
            return {"N": hex(self.N), "e": hex(self.E)}
        
        elif your_input['option'] == 'sign':
            msg_b = bytes.fromhex(your_input['msg'])
            if ADMIN_TOKEN in msg_b:
                return {"error": "Cannot sign an admin token"}
            msg_i = bytes_to_long(msg_b)
            return {"msg": your_input['msg'], "signature": hex(pow(msg_i, self.D, self.N))}
        
        elif your_input['option'] == 'verify':
            msg_b = bytes.fromhex(your_input['msg'])
            msg_i = bytes_to_long(msg_b)
            signature = int(your_input['signature'], 16)
            
            if msg_i < 0 or msg_i > self.N:
                return {"error": "Invalid message"}
            
            verified = pow(signature, self.E, self.N)
            if msg_i == verified:
                if long_to_bytes(msg_i) == ADMIN_TOKEN:
                    return {"response": FLAG}
                else:
                    return {"response": "Valid signature"}
            else:
                return {"response": "Invalid signature"}
        
        else:
            return {"error": "Invalid option, it must be among 'get_pubkey', 'sign' or 'verify'"}