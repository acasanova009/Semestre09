    .text                   @ Sección de código
    .global main            @ Punto de entrada del programa

main:
    push {lr}               @ (1) Guardar link register (porque estamos en 'main')

    mov r0, #10             @ (2) r0 = 10
    mov r1, #20             @ (3) r1 = 20
    add r2, r0, r1          @ (4) r2 = r0 + r1 = 30
    mov r3, #5              @ (5) r3 = 5
    mul r4, r2, r3          @ (6) r4 = r2 * r3 = 150
    sub r5, r4, #50         @ (7) r5 = r4 - 50 = 100
    mov r0, r5              @ (8) valor de retorno = r5
    pop {lr}                @ (9) restaurar lr
    bx lr                   @ (10) regresar al sistema con r0=100
