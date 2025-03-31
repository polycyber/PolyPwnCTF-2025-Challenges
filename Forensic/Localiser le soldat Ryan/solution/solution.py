# Inspired by https://www.geeksforgeeks.org/morse-code-translator-python/

import pyshark

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

def ttl_to_morse(ttl):
    if ttl == 84:
        return '.'
    elif ttl == 254:
        return '-'
    return None

def extract_morse_from_pcap(pcap_file):
    cap = pyshark.FileCapture(pcap_file, display_filter='icmp')

    morse_message = []
    prev_timestamp = None
    current_letter = []
    
    for packet in cap:
        if 'ICMP' in packet:
            ttl = int(packet.ip.ttl)
            timestamp = float(packet.sniff_time.timestamp())
            
            # If TTL is one of the morse one, add it to the message
            if ttl_to_morse(ttl):
                if prev_timestamp:
                    # time diff with the last packet
                    time_diff = timestamp - prev_timestamp
                    #Around 9-10 seconds to separate words
                    if time_diff >= 9:
                       if current_letter:
                          current_letter.append(' ')
                          morse_message.append(''.join(current_letter))
                          current_letter = []
                    #Around 4-5 seconds to separate letters
                    if time_diff >= 4:
                        if current_letter:
                            morse_message.append(''.join(current_letter))
                            current_letter = []
                # Add the right caracter to the letter
                current_letter.append(ttl_to_morse(ttl))
                prev_timestamp = timestamp

    # Add the last letter
    if current_letter:
        morse_message.append(''.join(current_letter))

    #Converts to string
    return ' '.join(morse_message)

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
   
if __name__ == '__main__':
    pcap_file = 'files/locatingprivateryan.pcap'
    morse_message = extract_morse_from_pcap(pcap_file)
    print("Morse Message:")
    print(morse_message)
    
    decoded_message = decrypt(morse_message)
    print("\nDecoded Message:")
    print(decoded_message)