    .text                  @ Área de código
    .global _start         @ Hacer visible el punto de entrada al linker

_start:                    @ ---- INICIO DEL PROGRAMA ----
    mov r1, #0x19          @ r1 = 0x19 (25 decimal)
    mov r2, #53            @ r2 = 53
    add r3, r2, r1         @ r3 = r2 + r1 = 53 + 25 = 78
    mov r0, r3             @ r0 = código de salida (exit code) -> 78
    mov r7, #1             @ r7 = número de llamada al sistema "exit" (Linux ARM EABI)
    svc 0                  @ invoca al kernel -> termina el programa con exit(r0)
                           @ ---- FIN DEL PROGRAMA ----

