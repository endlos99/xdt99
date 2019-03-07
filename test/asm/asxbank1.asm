* BANK SWITCHING

* L1 >0000r L2 >0010r A1/B1 >6000 A2 >6100 B2/C1 >6200
       
L1     DATA >1111
       DATA L1,L2        ; >0000r >0010r
       DATA A1,A2        ; >6000  >6100
       DATA B1,B2        ; >6000  >6200
       DATA C1           ; >6200
       
       AORG >6000,0
A1     DATA >2222
       DATA L1,L2
       DATA A1#,A2#
*      DATA B1#,B2#        ; CANNOT ACCESS
*      DATA C1#

       AORG >6200,2
C1     DATA >3333
       DATA L1,L2
*      DATA A1#,A2#        ; CANNOT ACCESS
*      DATA B1#,B#2
       DATA C1#

       AORG >6000,1
B1     DATA >4444
       DATA L1,L2
*      DATA A1#,A2#        ; CANNOT ACCESS
       DATA B1#,B2#
*      DATA C1#

B2     AORG >6200,1
       DATA >5555
       DATA L1,L2
*      DATA A1#,A2#        ; CANNOT ACCESS
       DATA B1#,B2#
*      DATA C1#

A2     AORG >6100,0
       DATA >6666
       DATA L1,L2
       DATA A1#,A2#
;      DATA B1#,B2#        ; CANNOT ACCESS
*      DATA C1#

       RORG
L2     DATA >FFFF

