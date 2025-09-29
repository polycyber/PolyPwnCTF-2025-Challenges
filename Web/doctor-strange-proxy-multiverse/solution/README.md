# Doctor Strange and the Multiverse of Proxies I

## Write-up FR

1. Un lien sur la page permet d'aller à /instructions/instructions.html
2. On peut regarder le code de la page pour voir que le nom des formes est en fait un nom de fichier html dans le même dossier.
3. On peut naviguer manuellement à /instructions/ pour révéler le directory listing
4. On y trouve le premier flag.

## Write-up EN

1. A link on the page takes you to /instructions/instructions.html
2. You can look at the code on the page to see that the name of the shapes is in fact the name of an html file in the same folder.
3. You can manually navigate to /instructions/ to reveal the directory listing
4. There you'll find the first flag.

## Flag

`polycyber{d1r3ct0ryyyyyyy_listing_43e4412af}`

# Doctor Strange and the Multiverse of Proxies II

## Write-up FR

1. Le directory listing révèle aussi un fichier png nommé comme le mouvement de la main.
2. Il faut en déduire qu'il s'agit du dessin à faire sur le canevas pour accéder à l'univers 16.
3. Il est pratiquement impossible de le dessiner tel quel, on peut observer la requête faite par le canevas quand on dessine dedans pour comprendre le format dans lequel il transmet les données.
4. Le format est une liste de points en JSON ordonnés par y croissant d'abord puis en x croissant pour chaque y.
5. Un script javascript peut rapidement être fait pour charger l'image .png découverte plus tôt et le convertir en liste de points. Le script est [ici](convert.html).
6. Avec OWASP Zap on peut intercepter la requête du canevas et remplacer la liste de points par nos propres points.
7. Un popup s'ouvre sur le navigateur avec des informations de connexions vers un SOCKS proxy et un flag comme mot de passe.

## Write-up EN

1. The directory listing also reveals a png file named after the hand movement.
2. From this we can deduce that this is the drawing to be made on the canvas to access Universe 16.
3. It is practically impossible to draw it as it is. You can observe the request made by the canvas when you draw in it to understand the format in which it transmits the data.
4. The format is a list of points in JSON ordered first by increasing y and then by increasing x for each y.
5. A javascript script can quickly be made to load the .png image discovered earlier and convert it to a list of points.
6. With OWASP Zap we can intercept the canvas request and replace the list of points with our own points. The script is [here](convert.html).
7. A popup opens in the browser with connection information to a proxy SOCKS and a flag as the password.

## Flag

`polycyber{welcome_to_the_multiverse}`

# Doctor Strange and the Multiverse of Proxies III

## Write-up FR

1. On configure le socks proxy dans OWASP Zap pour iorabu.ca:4269 avec l'authentification récupérée plus tôt.
2. On accède à http://uni_16 et on reçoit du texte encodé. Le texte ressemble à du HTML. Le Content-Type nous informe que c'est du HTML.
3. Il faut déduire que l'univers 16 communique avec nous en ROT16. On peut le déduire directement ou alors tester de décoder la page dans Cyberchef.
4. Puisque tout le site web et toutes ses pages sont en ROT16, l'approche la plus efficace est de programmer un petit script qui modifie les réponses en contenu lisible avant de les transférer. Le script doit être ajouté comme "HTTP Sender" script dans OWASP Zap, et son contenu peut être trouvé [ici](owasp_zap_rot16_dynamic_decode.js). Puisque seul le contenu HTML est transféré en ROT16, il est prudent d'ajouter une vérification pour éviter la rétroconversion si la réponse ne commence pas par "<". Une alternative serait potentiellement de décoder chaque page une par une, télécharger le site et tenter de l'utiliser comme ça, mais ce serait pénible et non recommandé.
5. On peut maintenant naviguer librement le site. La page d'accueil nous indique que la clé pour accéder au prochain univers réside dans le carpaccio à la betterave. On remarque l'onglet recettes. En le consultant, on voit que les recettes changent chaque jour. Une vérification des requêtes dans OWASP Zap montre que la recette du poulet est accédée via `/qfy/ckbjyluhiu/husyfu?ydjuhdqb_yt=gc7aa8r47fja9834hidornakk==`, ce qui est ROT16 décodé donne `/api/multiverse/recipe?internal_id=qm7kk8b47ptk9834rsnybxkuu==`. Donc, on comprend que les recettes peuvent être accédées par un id, mais on n'a pas celui du carpaccio à la betterave qu'on recherche.
6. Il faut se promener sur le site pour tomber sur la page Horoscope, où on voit que les horoscopes sont obtenus par des requêtes qui donnent dans leur réponse un `internal_id` pour chaque signe du zodiaque, de 0 à 11. Donc, on a maintenant des correspondances entre 0 et 11 puis les `internal_id` associés. On retrouve dans cette liste le même `internal_id` que celui de la recette de Poulet à l'orange. On en déduit qu'on peut réutiliser ces `internal_id` pour accéder aux recettes.
7. En tentant tous les `internal_id` (les 12) sur la page des recettes, on tombe que celui équivalent à 0 donne le flag, qui est le mot de passe pour le prochain SOCKS proxy.
8. Pour obtenir le nom d'utilisateur et l'adresse du prochain SOCKS proxy, il suffit de consultater la page de documentation à l'aide de la navigation. On y trouve un croquis dessiné par Doctor Strange avec toute l'information.


## Write-up EN

1. We configure the proxy socks in OWASP Zap for iorabu.ca:4269 with the authentication retrieved earlier.
2. We access http://uni_16 and receive encoded text. The text looks like HTML. The Content-Type Header indicates that this is HTML.
3. We have to deduce that Universe 16 is communicating with us in ROT16. We can deduce this directly or try to decode the page in Cyberchef.
4. Since the entire website and all its pages are in ROT16, the most effective approach is to program a small script that modifies the responses into readable content before transferring them. The script should be added as an ‘HTTP Sender’ script in OWASP Zap, and its contents can be found [here](owasp_zap_rot16_dynamic_decode.js). Since only HTML content is transferred in ROT16, it is prudent to add a check to avoid back-conversion if the response does not start with ‘<’. An alternative would potentially be to decode each page one by one, download the site and try to use it that way, but this would be tedious and not recommended.
5. The site is now free to browse. The home page tells us that the key to the next world is beetroot carpaccio. Then there's the recipes tab. If you look at it, you can see that the recipes change every day. A check of the requests in OWASP Zap shows that the chicken recipe is accessed via `/qfy/ckbjyluhiu/husyfu?ydjuhdqb_yt=gc7aa8r47fja9834hidornakk==`, which is ROT16 decoded to `/api/multiverse/recipe?internal_id=qm7kk8b47ptk9834rsnybxkuu==`. So we understand that recipes can be accessed by an id, but we don't have the beetroot carpaccio id we're looking for.
6. You have to wander around the site to come across the Horoscope page, where you can see that the horoscopes are obtained by queries which give an `internal_id` for each sign of the zodiac, from 0 to 11. So we now have matches between 0 and 11 and the associated `internal_id`. This list contains the same `internal_id` as the recipe for Orange Chicken. We can therefore deduce that we can re-use these `internal_id` to access the recipes.
7. Trying all the `internal_id` (all 12) on the recipes page, we find that the one equivalent to 0 gives the flag, which is the password for the next SOCKS proxy.
8. To obtain the user name and address of the next SOCKS proxy, simply consult the documentation page using the navigation. There's a sketch drawn by Doctor Strange with all the information.

## Flag

`polycyber{found_univers_16_a00032}`

# Doctor Strange and the Multiverse of Proxies IV

## Write-up FR

1. On change le SOCKS Proxy dans OWASP Zap pour le nouveau nom d'utilisateur ROT18(doctorstrange) et le mot de passe révélé grâce au carpaccio de betteraves.
2. On peut alors accéder à http://uni_18/rot18(universes), soit http://uni_18/mfanwjkwk.
3. On a l'erreur qu'il manque le X-Token header, qui pouvait être obtenu en cliquant sur le gros bouton arc-en-ciel dans l'univers 16. On peut donc ajouter à la requête `X-Token: lgcwfsha`.
4. L'univers 16 contenait des indications qu'il faut aussi ajouter un header `X-Limit: 10` pour éviter d'avoir trop de résultats. Avec les deux headers, l'API nous répond avec une liste d'univers.
5. Une injection SQL peut être faite facilement dans le header `X-Limit`, car on peut facilement concevoir que la requête prend la forme `SELECT * FROM tablename LIMIT {X-Limit};`. Surtout, en cas d'erreur, la réponse contient la query faite vers la base de données. Une validation minime est faite pour empêcher les mots "SELECT" et "select". On peut le bypass avec "sElect", par exemple. Notons que ROT18 est appliqué sur le contenu injecté, il faut donc donné en ROT8 les mots de l'injection SQL pour la réussir. L'injection permet d'ajouter directement une autre requête après la première - elle est assez triviale une fois qu'on a pensé à injecter dans `X-Limit`.
6. Avec le information_schema on peut trouver la table `secrets_of_the_universe`, dans laquelle se trouve le dernier flag.

## Write-up EN

1. Change the SOCKS Proxy in OWASP Zap to the new username ROT18(doctorstrange) and the password revealed by the beetroot carpaccio.
2. You can then access http://uni_18/rot18(universes), i.e. http://uni_18/mfanwjkwk.
3. We get the error that the X-Token header is missing, which could be obtained by clicking on the big rainbow button in universe 16. You can therefore add `X-Token: lgcwfsha` to the query.
4. Universe 16 contained indications that an `X-Limit: 10` header should also be added to avoid getting too many results. With both headers, the API responds with a list of universes.
5. An SQL injection can easily be made in the `X-Limit` header, because it's easy to imagine the query taking the form `SELECT * FROM tablename LIMIT {X-Limit};`. Above all, in the event of an error, the response contains the query made to the database. Minimal validation is performed to prevent the words ‘SELECT’ and ‘select’. This can be bypassed with ‘sElect’, for example. Note that ROT18 is applied on the injected content (all letters), you have to give the injetion payload with a ROT8 shift to succeed. Injection allows you to add another query directly after the first - it's fairly trivial once you've thought about injecting into `X-Limit`.
6. Using the information_schema, we can find the `secrets_of_the_universe` table, in which the last flag is found.

## Flag

`polycyber{polyverse_8d113abd}`
