* BANK SWITCHING

* L1 >6000 L2 >602A A1/B1 >6010 A2/B2/C1 >6020

       BANK ALL, >6000
L1     DATA >1111
       DATA L1,L2        ; >0000r >0010r
       DATA A1,A2        ; >6000  >6100
       DATA B1,B2        ; >6000  >6200
       DATA C1           ; >6200

       BANK 0, >6010
A1     DATA >2222
       DATA L1,L2
       DATA X#A1,X#A2
*      DATA X#B1,X#B2      ; CANNOT ACCESS
*      DATA X#C1

       BANK 2, >6020
C1     DATA >3333
       DATA L1,L2
*      DATA X#A1,X#A2      ; CANNOT ACCESS
*      DATA X#B1,X#B2
       DATA X#C1

       BANK 1, >6010
B1     DATA >4444
       DATA L1,L2
*      DATA X#A1,X#A2      ; CANNOT ACCESS
       DATA X#B1,X#B2
*      DATA X#C1

B2     BANK 1, >6020
       DATA >5555
       DATA L1,L2
*      DATA X#A1,X#A2      ; CANNOT ACCESS
       DATA X#B1,X#B2
*      DATA X#C1

A2     BANK 0, >6020
       DATA >6666
       DATA L1,L2
       DATA X#A1,X#A2
*      DATA X#B1,X#B2      ; CANNOT ACCESS
*      DATA X#C1

       BANK ALL
       RORG
L2     DATA >FFFF
 
       END
