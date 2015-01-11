*  TEST REGISTERS

        IDT 'ASREGS'

* LABELS

SFIRST
SLOAD
L1      MOV R1,R2
        A R3,R4
        S R5,R6
        C R7,R8
        MOV R9,R10
        A R11,R12
        S R13,R14
        C R15,R0

        CLR R0
        CLR *R1
        CLR *R2+
        CLR @1(R3)
        CLR @L1+10(R4)

        DATA R1
        DATA R15

* ERRORS
        
*E1     EQU R1                * BAD FWD REFERENCE
*       CLR R16               * INVALID REGISTER
*       CLR R>1               * INVALID REGISTER
*R2     DATA >FFFF            * MULTIPLE SYMBOLS
        
* END

SLAST
Z       END
