# TitaNIC

## Write-up FR

La capture réseau contient des requêtes DNS pour déterminer l'adresse IP du domaine `titanic.pirate` (le navigateur essaie automatique d'autres noms de domaines pour compléter la recherche: `www.titanic.pirate`,`titanic.pirate.home`). Mais ce TLD (*[Top Level Domain](https://fr.wikipedia.org/wiki/Domaine_de_premier_niveau)*) n'est pas administré par [l'ICANN](https://fr.wikipedia.org/wiki/Internet_Corporation_for_Assigned_Names_and_Numbers) et ses serveurs racines ne réussissent pas à résoudre le nom de domaine `titanic.pirate`. Mais ce TLD est administré par l'association OpenNIC qui est la principale [alternative aux racines de l'ICANN.](https://fr.wikipedia.org/wiki/Serveur_racine_alternatif_du_DNS)

Il faut donc résoudre ce nom de domaine en passant par OpenNIC plutôt que par l'ICANN. En regardant sur [leur site](https://opennic.org/) on trouve de nombreux serveurs DNS, on en prends un et on utilise `dig` pour résoudre `titanic.pirate`:

```bash
dig @168.235.111.72 titanic.pirate
```

Et on récupère bien l'adresse IP associée au nom de domaine:

```
;; QUESTION SECTION:
;titanic.pirate.      IN  A

;; ANSWER SECTION:
titanic.pirate.    86400  IN  A  137.184.160.172
```

On peut maintenant se rendre sur le site Web hébergé à cette adresse IP avec `curl` ou son navigateur préféré:

```bash
curl http://137.184.160.172
```

Et on trouve le flag sur la page d'accueil ! 🚩

## Write-up EN

The network capture contains DNS queries to determine the IP address of the domain `titanic.pirate` (the browser automatically tries other domain names to complete the search: `www.titanic.pirate`, `titanic.pirate.home`). However, this TLD (*[Top-Level Domain](https://en.wikipedia.org/wiki/Top-level_domain)*) is not managed by [ICANN](https://en.wikipedia.org/wiki/Internet_Corporation_for_Assigned_Names_and_Numbers), and its root servers fail to resolve the domain name `titanic.pirate`. Instead, this TLD is managed by the OpenNIC association, which is the main [alternative to ICANN's root servers](https://en.wikipedia.org/wiki/Alternative_DNS_root).

Therefore, this domain name must be resolved using OpenNIC rather than ICANN. Looking at [their website](https://opennic.org/), we can find many DNS servers. We choose one and use `dig` to resolve `titanic.pirate`:

```bash
dig @168.235.111.72 titanic.pirate
```

And we successfully retrieve the IP address associated with the domain name:

```
;; QUESTION SECTION:
;titanic.pirate.      IN  A

;; ANSWER SECTION:
titanic.pirate.    86400  IN  A  137.184.160.172
```

Now, we can visit the website hosted at this IP address using `curl` or our preferred browser:

```bash
curl http://137.184.160.172
```

And we find the flag on the homepage! 🚩

## Flag

`polycyber{4lt3rn4t1v3_DN5_r007_n3v3r_s1nk_unl1k3_T1t4n1c}`
