        .text                  @ Segmento de instrucciones (código ejecutable)
        .global _start         @ Marca la etiqueta _start como punto de entrada del programa

_start: 
        mov r0,#5              @ Cargar el valor 5 en r0
        mov r1,#0x01           @ Cargar el valor 1 en r1
        subs r3,r0,r1          @ r3 = r0 - r1 = 4; actualiza las banderas (Z, N, C, V)
        beq igual              @ Si el resultado fue 0 (Z=1), saltar a 'igual'
        bne diferente          @ Si el resultado no fue 0 (Z=0), saltar a 'diferente'

igual: 
        mov r0,#1              @ r0 = 1 → descriptor estándar de salida (stdout)
        ldr r1,=texto1         @ r1 = dirección de la cadena "texto1"
        mov r2,#30             @ r2 = número de bytes a escribir (30)
        mov r7,#4              @ r7 = código de syscall write
        svc 0                  @ Invocar al kernel: write(1, texto1, 30)
        b fin                  @ Saltar al final del programa

diferente: 
        mov r0,#1              @ r0 = 1 → descriptor estándar de salida (stdout)
        ldr r1,=texto2         @ r1 = dirección de la cadena "texto2"
        mov r2,#33             @ r2 = número de bytes a escribir (33)
        mov r7,#4              @ r7 = código de syscall write
        svc 0                  @ Invocar al kernel: write(1, texto2, 33)

fin: 
        mov r0,r3              @ r0 = valor de la resta (contenido de r3)
        mov r7,#1              @ r7 = código de syscall exit
        svc 0                  @ Terminar el programa con código de salida = r0

        .data                  @ Segmento de datos (almacena las cadenas en memoria)
texto1: .ascii "Datos iguales ... resultado = "    @ Mensaje mostrado si los valores eran iguales
texto2: .ascii "Datos diferentes ... resultado = " @ Mensaje mostrado si los valores eran distintos

