    .text
    .global main

main:
    push {lr}                 @ Guardar LR (porque estamos en 'main')

    ldr  r4, =DAT01           @ r4 = &DAT01
    ldr  r5, =DAT02           @ r5 = &DAT02
    ldrb r0, [r4]             @ r0 = DAT01 (8 bits, cero‑extendido)
    ldrb r1, [r5]             @ r1 = DAT02 (8 bits, cero‑extendido)

    add  r2, r0, r1           @ r2 = DAT01 + DAT02 (0..510)
    lsr  r0, r2, #1           @ r0 = r2 >> 1  (divide entre 2, entero)

    pop  {lr}                 @ Restaurar LR
    bx   lr                   @ return r0 (promedio)

    .data
DAT01: .byte 42               @ <-- Cambia aquí tus datos de 8 bits (0..255)
DAT02: .byte 77
