* XORG

* EACH BLOCK HAS 11 WORDS == >16 BYTES
* C 0000 B B000 C 002C B A000 B C000 B A040 B D000

A1
L1     DATA >1111         * >0000r
       DATA L1,L2,L3
       DATA L4,L5,L6,L7
       JMP  $
       B    @$

A2     XORG >B000
L2     DATA >2222         * >B000
       DATA L1,L2,L3
       DATA L4,L5,L6,L7
       JMP  $
       B    @$
L2T    JMP  L2T
       B    @L2T

A3     RORG
L3     DATA >3333         * >002Cr
       DATA L1,L2,L3
       DATA L4,L5,L6,L7
       JMP  $
       B    @$

A4     AORG >A000
L4     DATA >4444         * >A000
       DATA L1,L2,L3
       DATA L4,L5,L6,L7
       JMP  $
       B    @$

A5     XORG >C000
L5     DATA >5555         * >C000
       DATA L1,L2,L3
       DATA L4,L5,L6,L7
       JMP  $
       B    @$
L5T    JMP  L5T

A6     AORG >A040
L6     DATA >6666         * >A040
       DATA L1,L2,L3
       DATA L4,L5,L6,L7
       JMP  $
       B    @$

       RORG
A7     XORG >D000
L7     DATA >7777         * >D000
       DATA L1,L2,L3
       DATA L4,L5,L6,L7
       JMP  $
       B    @$
L7T    JMP  L7T
       B    @L7T

A8     XORG >2000
L8     DATA >8888
L8A    BSS  1
L8B    BSS  4
L8C    BES  4
L8D    BES  3
L8E    EQU  L8B-L8A+L8D-L8C
       BYTE 1
L8F    DATA L8,L8A,L8D,L8E,L8F
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
