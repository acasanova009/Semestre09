    .text
    .global main

main:
    push {lr}                 @ Guardar LR

    mov  r0, #0               @ r0 = 0  (contador principal)
    mov  r1, #9               @ r1 = 9  (límite superior)
    mov  r2, #0               @ r2 = 0  (umbral inferior para el segundo bucle)

loop1:                         @ ---- Contar de 0 a 9 ----
    add  r0, r0, #1           @ r0 = r0 + 1
    cmp  r1, r0               @ ¿r0 == 9?
    bne  loop1                @ si no, sigue incrementando

loop2:                         @ ---- Contar de 9 a 0 ----
    add  r0, r0, #-1          @ r0 = r0 - 1
    cmp  r2, r0               @ ¿r0 == 0?
    beq  loop1                @ si ya llegó a 0, vuelve a subir (ciclo infinito)
    b    loop2                @ si no, sigue bajando
