.global _start
_start:
    mov r1, #0x19     @ r1 = 25
    mov r2, #53       @ r2 = 53
    add r3, r2, r1    @ r3 = r2 + r1 = 78
    mov r0, r3        @ preparar valor de salida (78) en r0
    mov r7, #1        @ syscall 1 = exit
    svc 0             @ ejecutar llamada al sistema