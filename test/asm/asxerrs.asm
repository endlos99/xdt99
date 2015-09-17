*  ERROR HANDLING: xdt99 extensions

       idt 'ASXERRS'

       ; binary includes

bininc ibyte "nonexisting"    ;ERROR

       ; text bytes

text1  text >123456
       text >12x34            ;ERROR
       
       ; label continuations

label1:
label2:                       ;ERROR
       clr  0

label3:
       clr  0
label3 clr  1                 ;ERROR

label4 clr  0
label4:
       clr  1                 ;ERROR
       
       ; preprocessor

nolab  .ifdef 1               ;ERROR

       ; macros

       .defm mac1
       .endm
       .defm mac1             ;ERROR

       ,defm mac2
       clr  #2
       .endm
       .mac2 1                ;ERROR

       .macX                  ;ERROR

       .defm mac3
       .defm mac4             ;ERROR
       .endm

* NO ERRORS

good1:
       ; comment
       clr  0

       end
