    .text                  @ Sección de código del programa
    .global _start         @ Hace visible la etiqueta _start al linker (punto de entrada)

_start: 
    mov r0,#5              @ r0 = 5
    mov r1,#0x01           @ r1 = 1
    subs r3,r0,r1          @ r3 = r0 - r1 = 5 - 1 = 4 (actualiza banderas Z, N, C, V)
    beq igual              @ Si el resultado fue 0 (Z=1), salta a la etiqueta 'igual'
    bne diferente          @ Si el resultado no fue 0 (Z=0), salta a 'diferente'

igual: 
    mov r0,#1              @ r0 = descriptor de archivo (1 → stdout)
    ldr r1,=texto1         @ r1 = dirección de la cadena texto1
    mov r2,#30             @ r2 = longitud de la cadena (30 bytes)
    mov r7,#4              @ r7 = número de syscall 'write' en Linux ARM
    svc 0                  @ Llamada al sistema: write(1, texto1, 30)
    b fin                  @ Saltar al final del programa

diferente: 
    mov r0,#1              @ r0 = descriptor de archivo (1 → stdout)
    ldr r1,=texto2         @ r1 = dirección de la cadena texto2
    mov r2,#33             @ r2 = longitud de la cadena (33 bytes)
    mov r7,#4              @ r7 = número de syscall 'write'
    svc 0                  @ Llamada al sistema: write(1, texto2, 33)

fin: 
    mov r0,r3              @ r0 = valor de la resta (r3 = 4 en este caso)
    mov r7,#1              @ r7 = número de syscall 'exit'
    svc 0                  @ Termina el programa con código de salida r0

    .data                  @ Sección de datos (cadenas en memoria)
texto1: .ascii "Datos iguales ... resultado = "   @ Cadena para caso de igualdad
texto2: .ascii "Datos diferentes ... resultado = " @ Cadena para caso de desigualdad
