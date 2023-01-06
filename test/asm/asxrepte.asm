* .rept errors

       rorg

       .rept 5
       byte 1

       .defm foo              ;ERROR
       byte 2
       .endm                  ;ERROR
       .endr

       .rept r                ;ERROR
       byte 2
       .endr                  ;ERROR

       .endr                  ;ERROR

       .defm bar
       .rept 3                ;ERROR
       byte 3
       .endr                  ;ERROR
       .endm

       .bar

r:
       equ  3

       end
