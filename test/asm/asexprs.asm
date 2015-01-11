*  TEST EXPRESSIONS

        REF X1,X0
        DEF LABELX

* WELL-DEFINED VALUES (EQU)

        DATA >FFFF,>1111

E1      EQU >1
E2      EQU >100
*E0     EQU >10000            * OUT OF RANGE
E3      EQU ->100
*E0     EQU >-1               * SYNTAX ERROR
E4      EQU -0
E5      EQU '1'
E6      EQU '10'
E7      EQU -'10'
*E0     EQU '100'             * SYNTAX ERROR
E8      EQU ''
E9      EQU -''
E10     EQU +>FF00

E11     EQU 1+2*3-4/5+6
E12     EQU -1+-2*-3--4/-5
E13     EQU >1+>2*>3->4/>5+>6
E14     EQU ->1+->2*->3-->4/->5
E15     EQU '1'+-'2'*-'3'--'4'
E16     EQU 2+->10-' '+'+'''+001
E17     EQU ' ,'+'--'+''-'-*'+',+'
E18     EQU E2+E1*>10-10/>4
E19     EQU E1+0*0

E20     EQU >E000
E21     EQU E20+>1000
E22     EQU E20->1000
E23     EQU E20+>E000->1000
E24     EQU E20->F000->1000
E25     EQU E20/2
E26     EQU E20*2
E27     EQU E20/-2
E28     EQU E20*-2
E29     EQU E20/4*2/4*8

E30     EQU +E3
E31     EQU 1+++2
E32     EQU 1,2               * OK!
E33     EQU 1----2
E34     EQU 3+-++-+--2
E35     EQU 3*+-3
*E0     EQU 4+*3              * SYNTAX ERROR
*E0     EQU 4**3              * SYNTAX ERROR
E36     EQU $
E37     EQU $+>F0

*E0     EQU QQ                * UNDEFINED SYMBOL (OK?)
*E0     EQU 1/0               * OUT OF RANGE
*E0     EQU A1                * BAD FWD REF
*E0     EQU E0                * BAD FWD REF
*E0     EQU X1                * INVALID REF

*E0     EQU >aa               * SYNTAX ERROR
E41     EQU 'a'
E42     EQU -'aa'
*e42     EQU 'Aa'             * SYNTAX ERROR

E50     EQU 1+1
E51     EQU 2*E50             * == 4, != 3

EX      DATA E1,E2,E3,E4,E5
        DATA E6,E7,E8,E9,E10
        DATA E11,E12,E13,E14,E15
        DATA E16,E17,E18,E19,E20
        DATA E21,E22,E23,E24,E25
        DATA E26,E27,E28,E29,E30
        DATA E31,E32,E33,E34,E35
        DATA E41,E42,E51
FY      DATA F1,F2,F3,F4,F5
        DATA F6,F7,F8,F9,F10

*       BSS EX                * SYNTAX ERROR
        BSS FY-EX
        BSS $-FY

* LABELS

LABELX  DATA LABELX

* VALUES (DATA/BYTE)

D1      DATA 10,>10,-20,->20,0
        DATA ->FFFF,->7FFF,->8000
        DATA >7FFF*>FFFF,>7FFF*2
*       DATA >10000/4         * OUT OF RANGE (X)
        DATA 'A',-'b',',''',-'-F'
        DATA E1+E2*2-E5/E1
        DATA +++E5----E6*+-+-E1
        DATA R1+A1,R2+R3+A1-R1,A1+A2+A3+E1*2
        DATA $,$+>222,$+A1,A2-$+R1

B1      BYTE 10,>10
        BYTE >FFEE
        BYTE -10,->10,->80
*       BYTE ->FF             * OUT OF RANGE (X)
        BYTE >2*-2,>80+->80
        BYTE 400-300,>2000/>100
*       BYTE >FF*>7F          * OUT OF RANGE (X)
        BYTE A6
*       BYTE R1               * SYNTAX ERROR
        BYTE R3-R1,R1-R3
        BYTE A3-A1,A1-A3

* ADDRESSES (GA)

        DATA >FFFF,>2222
        
G1      INC 1
        INC >1
        INC E1
        INC E11
*       INC 1+2               * SYNTAX ERROR
*       INC ->FFFF            * SYNTAX ERROR
*       INC E1+1              * SYNTAX ERROR
*       INC 16                * INVALID REGISTER

G2      INC @1000
        INC @>1000
        INC @-1
        INC @''''
        INC @'XY'
        INC @-' '
        INC @','+'+'+'*'
        INC @E1
        INC @2+E1+>100-'A'
        INC @-E2+E4*2->10
        
G3      INC @R1
*       INC @-R1              * SYNTAX ERROR
        INC @R4
        INC @A1
        INC @-A1
        INC @R2->80+'A'
        INC @A3+128/2-A1
        INC @A1+R4-R1
        INC @R1+A4-A1
        INC @A4+R1-A1+1
        INC @R3+A2-R2+>2
        INC @R1+R2-R3
        INC @A1+A2-A3
*       INC @A1-R1            * SYNTAX ERROR
        INC @R1-A1
        INC @A1+A2
*       INC @R1+R2            * SYNTAX ERROR
        INC @R2+1-R1*2+A1
*       INC @R2*2-R1+A1       * SYNTAX ERROR
        INC @R1+R2+R3-R4-R5
        
* IMMEDIATES (IOP)

        DATA >FFFF,>3333

I1      LI 0,1
        LI 0,>10
        LI 0,-123
        LI 0,'10'
        LI 0,-' '''

I2      LI 0,E1
        LI 0,E1+1*3-4/2+E2
        LI 0,E2+-16*10-14/16-E1
        LI 0,>1+E3+>1/>2*>3->4
        LI 0,>10+E4+>11/>10*>13->24

I3      LI 0,A1
        LI 0,-A1
        LI 0,A2+E1*>2
        LI 0,A2-A1+A3
        LI 0,A1+A2/2
        LI 0,A5/4

I4      LI 0,R1
*       LI 0,-R1              * SYNTAX ERROR
        LI 0,R1+>10-10
        LI 0,R1+E1
*       LI 0,R1*2             * SYNTAX ERROR
*       LI 0,R1*2-R2          * SYNTAX ERROR
*       LI 0,R1+R2            * SYNTAX ERROR
        LI 0,R1-R2+R3
        LI 0,R2-R3*-4

I5      LI 0,R1+A1
*       LI 0,A1-R1            * SYNTAX ERROR
        LI 0,R1-R2+R3-R4
        LI 0,R1+R2-R3-R4
        LI 0,-R1+R2*2+R3

* REGISTER (WA)

        DATA >FFFF,>4444

W1      STST 0
        STST >A
*       STST ->FFFF           * SYNTAX ERROR
*       STST 16               * INVALID REGISTER
*       STST 1+1              * SYNTAX ERROR
        STST E1
*       STST E1+1             * SYNTAX ERROR
        STST F10
*       STST A2-A1            * INVALID REGISTER
*       STST R2-R1            * INVALID REGISTER

* RELATIVE JUMPS (DISP)

        DATA >FFFF,>5555

J1      JMP J2
J2      JMP J1
J3      JMP J3
        JMP J3-J2+J1
*       JMP J1+J2             * SYNTAX ERROR
        JMP J1+>2
        JMP R1
*       JMP A1                * OUT OF RANGE
        JMP J2+A1-A2
        JMP J3+R1-R2
*       JMP J1+A1-R1          * OUT OF RANGE

J4      JMP $
        JMP $+E1
        JMP >10+$
*       JMP -$                * OUT OF RANGE
        JMP $+4+J4-$
        JMP $+4-$+J4
*       JMP -2                * OUT OF RANGE BUT MAY YIELD >1080

* RELATIVE ADDRS

R1      DATA >11
R2      DATA >12
        RORG
R3      DATA >13
R4      DATA >14
R5      DATA >15

* ABSOLUTE ADDRS

        AORG >1000
A1      DATA >21
A2      DATA >22
A3      DATA >23
        AORG >1200
A4      DATA >24
        AORG >E000
A5      DATA >25

* RELATIVE JUMPS IN AORG

        AORG >0010
A6      DATA >FFFF,>6666

J10     JMP J10
        JMP >0010
        JMP J10*2
*       JMP R1*2              * SYNTAX ERROR
        RORG

* ADDRESS VALUES

        DATA >FFFF,>7777

F1      EQU R1
F2      EQU R2-R1+>100
F3      EQU A1
F4      EQU A3-A1+>100
F5      EQU A1+A2
*F0     EQU R1+R2             * SYNTAX ERROR
F6      EQU A1/4
F7      EQU A5/4
F8      EQU A1/-4
F9      EQU A5/-4

F10     EQU A2-A1             * == 2
*F0     EQU $+R1              * SYNTAX ERROR

FX      DATA F1,F2,F3,F4,F5
        DATA F6,F7,F8,F9,F10

* END

Z1      END
Z2      DATA >DEAD
Z3      DATA >C0DE

SLAST   EVEN
