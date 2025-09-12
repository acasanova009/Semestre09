        .text                  @ Sección de código
        .global _start         @ Exporta la etiqueta de entrada para el linker

_start:                        @ ---- INICIO ----
        mov   r1, #0x19        @ Carga 25 (0x19) en r1
        mov   r2, #53          @ Carga 53 en r2
        add   r3, r2, r1       @ r3 = r2 + r1  -> 78
        mov   r0, r3           @ Código de salida en r0 (convención: r0 = 1er argumento)
        mov   r7, #1           @ Número de syscall: 1 = exit (ABI Linux ARM)
        svc   0                @ Trap al kernel: exit(r0). Termina el programa
                               @ ---- FIN ----
