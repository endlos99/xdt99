*  TEST ERROR HANDLING

        IDT 'ASERRS'
        LIST

        DEF Q
        DEF E
        DEF E                 * MULTIPLE SYMBOLS ERROR
        REF QREF
        
E       EQU >1
X       DATA >FFFF

* SYNTAX ERRORS

        EQU
        DATA >,>
        DATA @
        DATA ,,,

        MOV
        MOV ,
        MOV 1
        MOV 1,
        MOV ,1
        MOV @>G,@>H
        MOV @,@
        MOV '

        CLR >
        CLR >G
        CLR -1
        CLR +1
        CLR 1(1)
        CLR 1()
        CLR @
        CLR @0()
        CLR @(1)
        CLR 1+
        CLR *+
        CLR *1+2
        CLR *1(2)
        CLR 'X'
        CLR '

        LI 0
        LI 0,
        LI 0,,1
        LI 0,>
        LI 0,@
        LI 0,@0()
        LI 0,@(1)
        LI 0,*+
        LI 0,'
        LI 0,-'
        LI 0,'''
        LI 0,-'''
        LI >G,1
        LI >,1
        LI -1,1
        LI 'X',1
        LI '

        LI 0,1*+2
        LI 0,/2+3
        LI 0,+*1
        LI 0,1**2

        * BAD COMMENT

* MISC ERRORS

        DATA QQ               * UNDEFINED SYMBOL ERROR
X       DATA >EEE1            * MULTIPLE SYMBOLS ERROR
E       DATA >EEE2            * MULTIPLE SYMBOLS ERROR
        DATA 1,,2             * SYNTAX ERROR
        DATA 1,               * SYNTAX ERROR
*lc1    EQU 1                 * SYNTAX ERROR (X)
*lc2    DATA 1                * SYNTAX ERROR (X)
*       DATA >aa              * SYNTAX ERROR (X)

S1      BAD                   * INVALID MNEMONIC
S2      BAD 1,1               * INVALID MNEMONIC

        CLR %

* LABELS

*LABEL1A EQU >1                * SYMBOL TRUNCATION WARNING (X)
*LABEL2A DATA >2               * SYMBOL TRUNCATION WARNING (X)

*LX     DATA LABEL1B,LABEL2B  * SYMBOL TRUNCATION WARNING (X)
*       DATA LX

* VALUE RANGES

V1      DATA 0
*       DATA 65536            * OUT OF RANGE (X)
*       DATA >100*>100        * OUT OF RANGE (X)
*       BYTE 256              * OUT OF RANGE (X)
*       BYTE '10'             * OUT OF RANGE (X)

* EQU EXPRS

E2      EQU Z                 * BAD FWD REFERENCE ERROR
E3      EQU QREF              * INVALID REF ERROR
*       EQU 1                 * SYNTAX ERROR (X)
E4      EQU
*                             ^ SYNTAX ERROR

*E10    EQU >10000            * OUT OF RANGE ERROR (X)
E11     EQU >-1               * SYNTAX ERROR
E12     EQU '100'             * SYNTAX ERROR
E13     EQU 1/0               * OUT OF RANGE ERROR

E20     EQU -                 * SYNTAX ERROR
E21     EQU 1+                * SYNTAX ERROR
E22     EQU *2                * SYNTAX ERROR

* OTHER DIRECTIVES

        BSS A-R               * BAD FWD REFERENCE
        BSS R                 * BAD FWD REFERENCE
        DATA QREF+2           * INVALID REF

* ADDRESS EXPRS

        DATA >FFFF,>1111

        INC 1+2               * SYNTAX ERROR
        INC ->FFFF            * SYNTAX ERROR
        INC E+1               * SYNTAX ERROR
        INC 16                * INVALID REGISTER ERROR

        INC @-R               * SYNTAX ERROR
        INC @A-R              * SYNTAX ERROR
        INC @R+R              * SYNTAX ERROR
        INC @R*2-R+A          * SYNTAX ERROR

* IMMEDIATES (IOP)

        DATA >FFFF,>2222

        LI 0,-R               * SYNTAX ERROR
        LI 0,R*2              * SYNTAX ERROR
        LI 0,R*2-R            * SYNTAX ERROR
        LI 0,R+R              * SYNTAX ERROR
        LI 0,A-R              * SYNTAX ERROR

* REGISTER (WA)

        DATA >FFFF,>3333

        STST ->FFFF           * SYNTAX ERROR
        STST 16               * INVALID REGISTER ERROR
        STST 1+1              * SYNTAX ERROR
        STST E1+1             * INVALID REGISTER ERROR
        STST A2-A1            * INVALID REGISTER ERROR
        STST R2-R1            * INVALID REGISTER ERROR

* RELATIVE JUMPS (DISP)

        DATA >FFFF,>4444

        JMP R+R               * SYNTAX ERROR
        JMP A                 * OUT OF RANGE ERROR
        JMP A-R               * SYNTAX ERROR

        JMP R*2               * SYNTAX ERROR

* REFERENCE ADDRESSES

R0      RORG
R       DATA >1111
RR      DATA >2222
A0      AORG >1000
A       DATA >3333
AA      DATA >4444
RZ      RORG

* END
        
Z       END

* ERRORS/NON-ERRORS NOT REPLICATED

*AB_C   DATA >EEE2            * SYNTAX ERROR
*AB_D   DATA >EEE3            * MULTIPLE SYMBOLS ERROR
*E1     EQU Q                 * UNDEFINED SYMBOL ERROR (FLAKY)
*       DEF                   * SYNTAX ERROR
*       BYTE                  * SYNTAX ERROR
*       TEXT                  * SYNTAX ERROR
*       DATA                  * SYNTAX ERROR

* UNSUPPORTED

*E      EQU 1,                * OK
*       DATA Q                * OK
*       JMP Q                 * OK
