from pwn import *

PAUSE = r"""

  _________
 /         \
|  ///  |\  |
|  /     L\ |
| /        \|
 \_________/

> 
"""

BON = r"""
  _________
 /         \
|           |
|   ----E   |
|   --==>   |
 \_________/

> 
"""

PARFAIT = r"""
  _________
 /         \
|     \\\|\ |
|       \ L\|
|        \  \
 \_________/

> 
"""

FINI = r"""
  _________
 /         \
|  |||  |\  |
|   |   |/  |
|   |   |   |
 \_________/

> 
"""

HOST = "localhost"
PORT = 1437

io = remote(HOST, PORT)

with open("../files/menu.txt", "r", encoding="utf-8") as f:
    MENU = [ligne.strip().lower() for ligne in f]

flag =""

response = io.recvuntil("\n> ").decode()

for plat in MENU:
    if(plat!="" and plat[0]!='-'):
        io.sendline(plat.encode())
        print(plat)
        response = io.recvuntil("\n> ").decode()
        print(response)
        if(response.strip() == PAUSE.strip()):
            response = io.recvuntil("\n> ").decode()
            print(response)
        if(response.strip() == BON.strip()):
            flag = flag + plat[0].lower()
        elif(response.strip() == PARFAIT.strip()):
            flag = flag + plat[0].upper()
        elif(FINI.strip() in response.strip()):
            flag = flag + plat[0]
            break

texte_final = io.recv().decode()
print(texte_final)
print(flag)
