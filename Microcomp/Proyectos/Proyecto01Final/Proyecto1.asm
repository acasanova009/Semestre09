;=======================================================================================
; ENCABEZADO CON ESPECIFICACIONES DEL C  DIGO, AUTOR Y FECHA
;=======================================================================================

;=======================================================================================
; LIBRERIAS
;=======================================================================================
#INCLUDE <P16F877A.INC>	;Librer  a para el microcontrolador utilizado

;=======================================================================================
; DECLARACI  N DE REGISTROS, CONSTANTES, ETC.
;=======================================================================================


;=======================================================================================
; VECTOR DE RESET
;=======================================================================================
	ORG 0
	GOTO INICIO
	
;=======================================================================================
; VECTOR DE INTERRUPCIONES
;=======================================================================================
	ORG 4
	GOTO ISR

;=======================================================================================
; CONFIGURACION DEL HARDWARE PARA EL PROYECTO
;=======================================================================================
INICIO:
	; Configurar PORTA como entradas digitales y, el PORTB como salidas digitales
	BSF STATUS, RP0	; Cambio al banco 1 de RAM (All   se encuentran los pines de configuraci  n del PORTA y PORTB)
	MOVLW 0X06
	MOVWF ADCON1	; Deshabilitamos los canales de entrada al CAD, los del PORTA ser  n digitales
	
	MOVLW 0X3F		; W <---0x3F
	MOVWF TRISA		; (TRISA) <---- todos los pines del PORTA ser  n entradas
	
	CLRF TRISB		; Todos los pines del PORTB ser  n salidas
	BCF STATUS, RP0	; Regresa al banco 0 de RAM
	CLRF PORTB		; Apaga todos los pines de PORTB

;=======================================================================================
; DECLARACI  N DE VARIABLES
;=======================================================================================
	CBLOCK 0x20		; Bloque de memoria general para variables
		CONT1		; Contador para retardos
		CONT2		; Segundo contador para retardos
		CONTADOR	; Variable para el contador binario
		TEMP		; Variable temporal para secuencias
		AUX			; Auxiliar para desplazamientos
	ENDC

;=======================================================================================
; PROGRAMA PRINCIPAL
;=======================================================================================
LOOP
	MOVF PORTA, W	; W <---- (PORTA)	
	ANDLW 0X03		; W <---- W AND 0000 0011
	ADDWF PCL, F	; (Parte baja del Program Counter, PCL) <---- W

	GOTO ETIQ1		; PORTA = 0x00 -> Parpadeo de LED
	GOTO ETIQ2		; PORTA = 0x01 -> Contador binario desde 0 hasta 18
	GOTO ETIQ3		; PORTA = 0x02 -> Secuencia sencilla
	GOTO ETIQ4		; PORTA = 0x03 -> Corrimiento de dos LEDs


ETIQ1:
	CLRF PORTB
	BSF PORTB, 0                  ; Enciende LED en RB0
	CALL RETARDO_500MS         ; Espera 500 ms
	BCF PORTB, 0                  ; Apaga LED
	CALL RETARDO_500MS         ; Espera 500 ms
	GOTO LOOP

ETIQ2:
	CLRF PORTB
	CLRF CONTADOR                  ; Inicializa contador en 0
CONTAR:
	MOVF CONTADOR, W
	MOVWF PORTB                    ; Muestra el valor en PORTB
	CALL RETARDO_300MS         ; Retardo para visualizaci  n
	INCF CONTADOR, F            ; Incrementa el contador
	MOVF CONTADOR, W
	SUBLW D'19'                    ; Compara si lleg   a 19 para reiniciar
	BTFSS STATUS, Z
	GOTO CONTAR                    ; Si no ha llegado, sigue contando
	GOTO LOOP                       ; Reinicia lectura de PORTA



ETIQ3:
	MOVLW 0x01
	MOVWF TEMP                     ; Patr  n inicial: 00000001
	CLRF PORTB
SECUENCIA:
	MOVF TEMP, W
	MOVWF PORTB                    ; Muestra patr  n en PORTB
	CALL RETARDO_500MS         ; Retardo de 500 ms
	CALL RETARDO_1S              ; Retardo adicional de 1 s
	RLF TEMP, F                    ; Desplaza el bit a la izquierda
	BTFSC STATUS, C              ; Si el bit m  s alto se fue al carry, reinicia
	GOTO LOOP
	GOTO SECUENCIA               ; Contin  a la secuencia


ETIQ4:
    CLRF PORTB
    MOVLW b'11000000'          ; Patrón inicial (dos LEDs a la izquierda)
    MOVWF TEMP
    MOVLW D'7'                 ; 6 corrimientos en total
    MOVWF CONTADOR             ; Usamos CONTADOR como número de pasos

CORRER:
    MOVF TEMP, W
    MOVWF PORTB                ; Mostrar patrón
    CALL RETARDO_100MS         ; Retardo de 100 ms

    ; Corrimiento lógico a la derecha
    BCF STATUS, C              ; Asegura corrimiento lógico (entra 0 por bit7)
    RRF TEMP, F                ; TEMP >> 1

    DECFSZ CONTADOR, F         ; ¿Ya se hicieron los 6 pasos?
    GOTO CORRER                ; No ? seguir corrimiento

    GOTO LOOP                  ; Sí ? volver a leer switches

;=======================================================================================
; SUBRUTINAS
;=======================================================================================
RETARDO_100MS:
	MOVLW D'80'
	MOVWF CONT1
R100_1:
	MOVLW D'255'
	MOVWF CONT2
R100_2:
	NOP
	NOP
	DECFSZ CONT2, F
	GOTO R100_2
	DECFSZ CONT1, F
	GOTO R100_1
	RETURN

RETARDO_300MS:
	MOVLW D'150'
	MOVWF CONT1
R300_1:
	MOVLW D'255'
	MOVWF CONT2
R300_2:
	NOP
	NOP
	DECFSZ CONT2, F
	GOTO R300_2
	DECFSZ CONT1, F
	GOTO R300_1
	RETURN

RETARDO_500MS:
	MOVLW D'200'
	MOVWF CONT1
R500_1:
	MOVLW D'255'
	MOVWF CONT2
R500_2:
	NOP
	NOP
	DECFSZ CONT2, F
	GOTO R500_2
	DECFSZ CONT1, F
	GOTO R500_1
	RETURN

RETARDO_1S:
	MOVLW D'200'
	MOVWF CONT1
R1S_1:
	MOVLW D'255'
	MOVWF CONT2
R1S_2:
	NOP
	NOP
	NOP
	DECFSZ CONT2, F
	GOTO R1S_2
	DECFSZ CONT1, F
	GOTO R1S_1
	RETURN

;=======================================================================================
; ISR'S (Rutinas de servicio de interrupci  n)
;=======================================================================================
ISR:
	NOP			;Pierde un ciclo de m  quina
	RETFIE		; Retorno de la ISR

;=======================================================================================
; FIN DEL PROGRAMA
;=======================================================================================
	END			; Directiva de fin del programa

;=======================================================================================