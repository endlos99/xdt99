* macro errors

       aorg >2000

       .defm m1
       .endm

       .defm m1               ;ERROR
       .endm

       .endm                  ;ERROR

       .defm ifdef            ;ERROR
       .endm

       .else                  ;ERROR
       .endif                 ;ERROR

       .error                 ;ERROR

       .defm m2
       .defm m3               ;ERROR
       .endm

       end
