import random
import re
import string
from pwn import *

def reset_knowledge(passcode_length=6):
    knowledge = {letter: [i for i in range(passcode_length)] for letter in string.ascii_lowercase}
    return knowledge

def update_knowledge(knowledge, guess, correct, misplaced):
    for i, letter in enumerate(guess):
        if letter in correct:
            knowledge[letter] = [i]
        elif letter in misplaced:
            if i in knowledge[letter]:
                knowledge[letter].remove(i)
        else:
            if letter in knowledge:
                knowledge.pop(letter)
    return knowledge


def get_guess(knowledge, passcode_length=6):
    # Get the letter with the least amount of possibilities
    guess = [None] * passcode_length
    letters = sorted(knowledge, key=lambda x: len(knowledge[x]))
    letters_1 = [letter for letter in letters if len(knowledge[letter]) == 1]
    letters_other = [letter for letter in letters if len(knowledge[letter]) > 1]
    for letter in letters_1:
        guess[knowledge[letter][0]] = letter
    
    # Fill in the rest of the guess with random letters
    for i, letter in enumerate(guess):
        if letter is None:
            choice = random.choices(letters_other, weights=[1/len(knowledge[letter]) for letter in letters_other])[0]
            while choice in guess:
                choice = random.choices(letters_other, weights=[1/len(knowledge[letter]) for letter in letters_other])[0]
            guess[i] = choice
    guess = "".join(guess)
    return guess

    

HOST = "localhost"
PORT = 1337

passcode_length = 6
n_guesses = 5

io = remote(HOST, PORT)

for i in range(n_guesses):
    knowledge = reset_knowledge(passcode_length)
    if i == 0:
        response = io.recvuntil(">> ").decode()
        print(response)
    while True:
        guess = get_guess(knowledge, passcode_length)
        io.sendline(guess.encode())

        response = io.recv().decode()
        print(response)

        if "Impressive" in response:
            # We found a passcode
            break

        # Regex to extract letters well-placed
        well_placed = re.findall(r"Correctly placed letters\s*:\s*([a-z](?:-[a-z])*)", response)
        well_placed = [letter for group in well_placed for letter in group.split("-")]
        # Regex to extract letters misplaced
        misplaced = re.findall(r"Misplaced letters\s*:\s*([a-z](?:-[a-z])*)", response)
        misplaced = [letter for group in misplaced for letter in group.split("-")]
        knowledge = update_knowledge(knowledge, guess, well_placed, misplaced)
    


