.section .text
.global help

help:
    popq %rdi
    ret
    popq %rdx
    ret
    popq %rsi
    ret

.section .note.GNU-stack,"",%progbits
