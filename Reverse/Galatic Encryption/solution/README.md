# Be a jedi

## Write-up FR

Le binaire est un exécutable ELF x86_64. Lorsqu'on l'exécute, rien ne semble se produire.

Analysons-le avec Ghidra :
```c
bool FUN_001013b2(int param_1,long param_2)

{
  int iVar1;
  long lVar2;
  
  if (param_1 != 2) {
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  lVar2 = ptrace(PTRACE_TRACEME,0,0,0);
  if (lVar2 == -1) {
    puts("You will never get my passwor sith !");
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  iVar1 = FUN_001011c9(*(undefined8 *)(param_2 + 8));
  if (iVar1 == 0) {
    puts("Dont share my secret password");
  }
  else {
    puts("Are you a sith?");
  }
  return iVar1 != 0;
}
```
On constate que le programme attend un argument `password`, qu'il passe ensuite à la fonction `FUN_001011c9`.
On remarque également une protection anti-debug avec `ptrace(PTRACE_TRACEME, 0, 0, 0);`.

Regardons maintenant le code de `FUN_001011c9` :
```c
undefined8 FUN_001011c9(char *param_1)

{
  size_t sVar1;
  undefined8 uVar2;
  long in_FS_OFFSET;
  uint local_bc;
  int local_a8 [38];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_a8[0] = 10;
  local_a8[1] = 0x29;
  local_a8[2] = 0x35;
  local_a8[3] = 0xc;
  local_a8[4] = 0x24;
  local_a8[5] = 0xc;
  local_a8[6] = 0x22;
  local_a8[7] = 9;
  local_a8[8] = 0x3b;
  local_a8[9] = 0xd;
  local_a8[10] = 0x3f;
  local_a8[0xb] = 0xc;
  local_a8[0xc] = 3;
  local_a8[0xd] = 0x38;
  local_a8[0xe] = 0x51;
  local_a8[0xf] = 0x24;
  local_a8[0x10] = 0x3b;
  local_a8[0x11] = 0x51;
  local_a8[0x12] = 0x32;
  local_a8[0x13] = 3;
  local_a8[0x14] = 0x3b;
  local_a8[0x15] = 0x51;
  local_a8[0x16] = 0x22;
  local_a8[0x17] = 0x51;
  local_a8[0x18] = 0x35;
  local_a8[0x19] = 3;
  local_a8[0x1a] = 10;
  local_a8[0x1b] = 0x54;
  local_a8[0x1c] = 0x38;
  local_a8[0x1d] = 0x38;
  local_a8[0x1e] = 0x50;
  local_a8[0x1f] = 0x56;
  local_a8[0x20] = 0x3b;
  local_a8[0x21] = 0xb;
  local_a8[0x22] = 0x48;
  sVar1 = strlen(param_1);
  if (sVar1 == 0x23) {
    for (local_bc = 0; local_bc < 0x23; local_bc = local_bc + 1) {
      if (param_1[(int)local_bc] !=
          "5/7_-j>PDepdy{V=1R8(aON,IH`W2+!.#Qb6ch&A4oSMkxzn<)tEZlUis:KrTfFmGJX~Cq9v}^Y?|*g;w3uL@$0\' B"
          [local_a8[(int)local_bc]]) {
        uVar2 = 1;
        goto LAB_0010139c;
      }
    }
    uVar2 = 0;
  }
  else {
    uVar2 = 1;
  }
LAB_0010139c:
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return uVar2;
}
```
On remarque que le mot de passe doit être de longueur `0x23` (35 caractères).
Ensuite, il est comparé à une chaîne cachée à l'aide d'un tableau d'indices (local_a8).

Mais ce n'est pas très compliqué de comprendre que pour retrouver le bon password il suffit juste de faire : 
```c
for (local_bc = 0; local_bc < 0x23; local_bc = local_bc + 1) {
    printf("%c", "5/7_-j>PDepdy{V=1R8(aON,IH`W2+!.#Qb6ch&A4oSMkxzn<)tEZlUis:KrTfFmGJX~Cq9v}^Y?|*g;w3uL@$0\' B"[local_a8[(int)local_bc]]);
    }
```


## Write-up EN

The binary is an ELF x86_64 executable. When executed, nothing seems to happen.
Let's analyze it with Ghidra :
```c
bool FUN_001013b2(int param_1,long param_2)

{
  int iVar1;
  long lVar2;
  
  if (param_1 != 2) {
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  lVar2 = ptrace(PTRACE_TRACEME,0,0,0);
  if (lVar2 == -1) {
    puts("You will never get my passwor sith !");
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  iVar1 = FUN_001011c9(*(undefined8 *)(param_2 + 8));
  if (iVar1 == 0) {
    puts("Dont share my secret password");
  }
  else {
    puts("Are you a sith?");
  }
  return iVar1 != 0;
}
```
The program expects a password as an argument and passes it to the function `FUN_001011c9`.
There is an anti-debugging mechanism with `ptrace(PTRACE_TRACEME, 0, 0, 0)`. If a debugger is detected, the program exits.

```c
undefined8 FUN_001011c9(char *param_1)

{
  size_t sVar1;
  undefined8 uVar2;
  long in_FS_OFFSET;
  uint local_bc;
  int local_a8 [38];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_a8[0] = 10;
  local_a8[1] = 0x29;
  local_a8[2] = 0x35;
  local_a8[3] = 0xc;
  local_a8[4] = 0x24;
  local_a8[5] = 0xc;
  local_a8[6] = 0x22;
  local_a8[7] = 9;
  local_a8[8] = 0x3b;
  local_a8[9] = 0xd;
  local_a8[10] = 0x3f;
  local_a8[0xb] = 0xc;
  local_a8[0xc] = 3;
  local_a8[0xd] = 0x38;
  local_a8[0xe] = 0x51;
  local_a8[0xf] = 0x24;
  local_a8[0x10] = 0x3b;
  local_a8[0x11] = 0x51;
  local_a8[0x12] = 0x32;
  local_a8[0x13] = 3;
  local_a8[0x14] = 0x3b;
  local_a8[0x15] = 0x51;
  local_a8[0x16] = 0x22;
  local_a8[0x17] = 0x51;
  local_a8[0x18] = 0x35;
  local_a8[0x19] = 3;
  local_a8[0x1a] = 10;
  local_a8[0x1b] = 0x54;
  local_a8[0x1c] = 0x38;
  local_a8[0x1d] = 0x38;
  local_a8[0x1e] = 0x50;
  local_a8[0x1f] = 0x56;
  local_a8[0x20] = 0x3b;
  local_a8[0x21] = 0xb;
  local_a8[0x22] = 0x48;
  sVar1 = strlen(param_1);
  if (sVar1 == 0x23) {
    for (local_bc = 0; local_bc < 0x23; local_bc = local_bc + 1) {
      if (param_1[(int)local_bc] !=
          "5/7_-j>PDepdy{V=1R8(aON,IH`W2+!.#Qb6ch&A4oSMkxzn<)tEZlUis:KrTfFmGJX~Cq9v}^Y?|*g;w3uL@$0\' B"
          [local_a8[(int)local_bc]]) {
        uVar2 = 1;
        goto LAB_0010139c;
      }
    }
    uVar2 = 0;
  }
  else {
    uVar2 = 1;
  }
LAB_0010139c:
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return uVar2;
}
```
The password must be 35 characters long (0x23 in hex).
The program compares each character with a hidden string using an index table (local_a8).
To retrieve the correct password, we simply reconstruct it using the given character mappings :
```c
for (local_bc = 0; local_bc < 0x23; local_bc = local_bc + 1) {
    printf("%c", "5/7_-j>PDepdy{V=1R8(aON,IH`W2+!.#Qb6ch&A4oSMkxzn<)tEZlUis:KrTfFmGJX~Cq9v}^Y?|*g;w3uL@$0\' B"[local_a8[(int)local_bc]]);
    }
```

## Flag

`polycyber{my_s3cr3t_r3b3l_p@ssw0rd}`