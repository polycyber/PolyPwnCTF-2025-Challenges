import random
import re
import string
from pwn import *
from minizinc import Instance, Model, Solver


def make_model(guesses_feedbacks, n_attempts, passcode_length):
    model = Model("./solution.mzn")
    model["n"] = passcode_length
    model["n_attemps"] = n_attempts -1
    model["essais"] = list(map(lambda x : list(map(lambda l : string.ascii_lowercase.index(l)+1, x)), guesses_feedbacks.keys()))
    model["feedback"] = list(guesses_feedbacks.values())
    return model

def get_guess(passcode_length):
    return ''.join(random.sample(string.ascii_lowercase, k=passcode_length))

HOST = "localhost"
PORT = 1338

passcode_length = 6
n_attempts = 20
n_passcodes = 5

io = remote(HOST, PORT)

gecode = Solver.lookup("gecode")

for i in range(n_passcodes):
    guesses_feedbacks = {}


    response = io.recvuntil(">> ").decode()
    print(response)

    for j in range(n_attempts-1):
        guess = get_guess(passcode_length)
        io.sendline(guess.encode())

        response = io.recv().decode()
        print(response)

        # Regex to extract letters well-placed
        feedback = re.findall(r'\d+', response)
        guesses_feedbacks[guess] = list(map(int, feedback))

    model = make_model(guesses_feedbacks, n_attempts, passcode_length)
    instance = Instance(gecode, model)
    result = instance.solve(all_solutions=False)
    password = result["password"]
    password = ''.join(list(map(lambda x : string.ascii_lowercase[x-1], password)))
    print(password)
    io.sendline(password.encode())

response = io.recv().decode()
print(response)