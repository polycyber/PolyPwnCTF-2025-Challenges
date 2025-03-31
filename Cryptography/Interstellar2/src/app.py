from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.PublicKey import RSA
import signal, json

FLAG = 'polycyber{S1gn4tur3_1s_1mp0rt4nt_bu7_n0t_4lw4ys_s3cur3}'
ADMIN_TOKEN = b"Thorne=GOAT"

class Challenge():
    def __init__(self):
        myKey = RSA.generate(2048)
        self.N = myKey.n
        self.E = myKey.e
        self.D = myKey.d
        self.timeout = 1000

    def welcome(self):
        print('Please verify your RSA signature before continuing.')
        print('Choose an option: “get_pubkey”, “sign” or “verify”')
        print('Warning: you cannot sign an admin token!')
        print()
    
    def gameOver(self):
        print("Verification failed.")
    
    def success(self):
        print("Verification succed! You can continue: " + FLAG)
        
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

    def chall(self):
        self.welcome()
        signal.alarm(self.timeout)
        try:
            while True:
                user_input = input("\n- Enter your request: \n")
                try:
                    request = json.loads(user_input)
                    response = self.challenge(request)
                    if 'response' in response and response['response'] == FLAG:
                        self.success()
                        return
                    else:
                        print(json.dumps(response))
                        if "error" in response:
                            self.gameOver()
                            return
                except Exception as e:
                    print("Fatal error: ", e)
                    self.gameOver()
                    return
        finally:
            signal.alarm(0)
            
def timeout_handler(signum, frame):
    print("Too slow! Timeout!")
    exit(0)
    

if __name__ == '__main__':
    signal.signal(signal.SIGALRM, timeout_handler)
    server = Challenge()
    server.chall()
