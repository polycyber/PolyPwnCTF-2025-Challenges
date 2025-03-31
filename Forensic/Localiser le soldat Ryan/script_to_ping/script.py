#Inspired by https://www.geeksforgeeks.org/morse-code-translator-python/
# Dictionary representing the morse code chart
import time
from ping3 import ping

MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}
 
# Function to encrypt the string
# according to the morse code chart
def encrypt(message):
    cipher = ''
    for letter in message:
        if letter != ' ':
 
            # Looks up the dictionary and adds the
            # corresponding morse code
            # along with a space to separate
            # morse codes for different characters
            cipher += MORSE_CODE_DICT[letter] + ' '
        else:
            # 1 space indicates different characters
            # and 2 indicates different words
            cipher += ' '
 
    return cipher


def decrypt(message):
 
    # extra space added at the end to access the
    # last morse code
    message += ' '
 
    decipher = ''
    citext = ''
    for letter in message:
 
        # checks for space
        if (letter != ' '):
 
            # counter to keep track of space
            i = 0
 
            # storing morse code of a single character
            citext += letter
 
        # in case of space
        else:
            # if i = 1 that indicates a new character
            i += 1
 
            # if i = 2 that indicates a new word
            if i == 2 :
 
                 # adding space to separate words
                decipher += ' '
            else:
 
                # accessing the keys using their values (reverse of encryption)
                decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT
                .values()).index(citext)]
                citext = ''
 
    return decipher



def send_ping(host="192.168.56.101", message='', interval=5):
    """Send a single ping in a loop."""
    for letter in message:
        if letter == '.':
            response_time = ping(host, ttl=85)
        elif letter == '-':
            response_time = ping(host, ttl=255)
        elif letter == ' ':
            time.sleep(interval)
        if response_time is not None:
            print(f"Ping to {host}: {response_time:.2f} ms")
        else:
            print(f"Ping to {host} failed.")

if __name__ == "__main__":
    initial_message = "THE 101ST AIRBORNE DIVISION IS GOING TO TAKE ROMEO ALFA MIKE ECHO LIMA LIMA ECHO. THE FLAG IS POLYCYBER-G0S4V3PRIVAT3RY4N"
    morse_message = encrypt(initial_message)
    send_ping(message=morse_message)