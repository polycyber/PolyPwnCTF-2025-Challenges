# HackToTheFuture - Secrets writeup

By opening the game in IDA/Ghidra, and looking for `ASSETS.GAK` in the strings, we can find an Xref in a function that seems to setup the game.
If we go up a bit in the function, we can see a series of Xor operations, probably some encryption. By reversing these operations, we obtain the string: `2015r0ckz!!`.

If we try to open the `ASSETS.GAK` file with `7z`, we can use this as the password, and we can decrypt its contents.

If we open `data/level1/mall.obj` in a text editor, we can see `polycyber{alW4ys_s0m3Th1nG_h1Dd3N}` in there.