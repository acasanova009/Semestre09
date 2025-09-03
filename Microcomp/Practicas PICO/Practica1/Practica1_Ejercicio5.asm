PROCESSOR 16f877 
 INCLUDE  <p16f877.inc>    
 
J equ H'26'   
K equ       H'27' 
C1 equ H'28' 
R1 equ H'29' 
 
  ORG 0 
              GOTO  INICIO               
 
             ORG 5 
INICIO:

	
    MOVF J, W ; W = J
	SUBLW .32 ; W = 32 - W
	;W = ? Es cero o NO?
	BTFSC STATUS, Z ; Si Z se prende => Z = 1
	GOTO YA_ES_VEINTE

INCF J, 1 ;J++
	MOVF J, W ; W = J
	SUBLW .9 ; W = 9 - W
	;W = ? Es cero o NO?
	BTFSC STATUS, Z ; Si Z se prende => Z = 1
	GOTO YA_ES_NUEVE

NO_ES_NUEVE:
	MOVF J, W ; W = J
	SUBLW .25 ; W = 25 - W
	;W = ? Es cero o NO?
	BTFSC STATUS, Z ; Si Z se prende => Z = 1
	GOTO YA_ES_Diecinueve

NO_YA_ES_Diecinueve

	NOP
	GOTO INICIO

YA_ES_Diecinueve
	ADDLW .32 ;Ya W = 32
	MOVWF J
	GOTO INICIO 
		

YA_ES_NUEVE:
	ADDLW .16 ;Ya W = 16
	MOVWF J
	GOTO INICIO 
		
YA_ES_VEINTE:
	CLRF J
	CLRW
	GOTO INICIO

	
	END