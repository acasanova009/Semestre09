    .text
    .global main

main:
    push {lr}              @ Guardar LR (porque estamos en 'main')

    mov r0, #1             @ Inicia con 000...0001 (solo el bit 0 en 1)
    mov r1, #32            @ Número de bits de un registro (32 pasos)
    
loop:
    lsl r0, r0, #1         @ Desplaza r0 una posición a la izquierda
    subs r1, r1, #1        @ r1 = r1 - 1 (contador de pasos)
    bne loop               @ Si r1 != 0, repetir

    @ Cuando termina, r0 = 0 (bit salió del MSB)
    mov r0, #0             @ Valor de retorno (opcional)
    pop {lr}
    bx lr
