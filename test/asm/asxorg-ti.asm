* XORG

* EACH BLOCK HAS 11 WORDS == >16 BYTES
* C 0000 B B000 C 002C B A000 B C000 B A040 B D000

A1
L1     DATA >1111
       DATA L1,L2,L3
       DATA L4,L5,L6,L7
       JMP  L1+16
       B    @L1+18

*      XORG >B000
A2     RORG
L2     EQU  >B000
L2X    DATA >2222
       DATA L1,L2,L3
       DATA L4,L5,L6,L7
       JMP  L2X+16
       B    @L2X+18

A3     RORG
L3     DATA >3333
       DATA L1,L2,L3
       DATA L4,L5,L6,L7
       JMP  L3+16
       B    @L3+18

A4     AORG >A000
L4     DATA >4444
       DATA L1,L2,L3
       DATA L4,L5,L6,L7
       JMP  L4+16
       B    @L4+18

*      XORG >C000
A5     AORG >A016
L5     EQU  >C000
L5X    DATA >5555
       DATA L1,L2,L3
       DATA L4,L5,L6,L7
       JMP  L5X+16
       B    @L5X+18

A6     AORG >A040
L6     DATA >6666
       DATA L1,L2,L3
       DATA L4,L5,L6,L7
       JMP  L6+16
       B    @L6+18

       RORG
*      XORG >D000
A7     RORG
L7     EQU  >D000
L7X    DATA >7777
       DATA L1,L2,L3
       DATA L4,L5,L6,L7
       JMP  L7X+16
       B    @L7X+18

*      XORG >2000
A8     RORG
L8     EQU  >2000
L8X    DATA >8888
L8A    EQU  L8+2
L8AX   BSS  1
L8B    EQU  L8A+1
L8BX   BSS  4
L8C    EQU  L8B+4+4
L8CX   BES  4
L8D    EQU  L8C+3
L8DX   BES  3
L8E    EQU  L8B-L8A+L8D-L8C
       BYTE 1
L8F    EQU  L8D+2
L8FX   DATA L8,L8A,L8D,L8E,L8F
       MOV  @L8A,@L8D
       LI   0,L8B

       RORG
       DATA >FFFF
       DATA L2-L4
       DATA L5-L4
       DATA L7-L4
       DATA L7-L2+L7-L5
       DATA L5-L7+L2

       DATA A1,A2,A3,A4
       DATA A5,A6,A7,A8
       
E1     EQU  L1
E2     EQU  L2
E3     EQU  L3
E4     EQU  L4
E5     EQU  L5
E6     EQU  L6
E7     EQU  L7
*E10   EQU  L2-L1    * ILLEGAL
*E11   EQU  L3-L2
E21    EQU  L5-L4
E22    EQU  L6-L5
E31    EQU  L5-L2
E32    EQU  L8-L5
E33    EQU  L8-L2
E41    EQU  L2-L4
E42    EQU  L5-L4
E43    EQU  L4-L8

       DATA E1,E2,E3,E4,E5,E6,E7
       DATA E21,E22
       DATA E31,E32,E33
       DATA E41,E42,E43
       
       END
