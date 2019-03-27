*  ERROR HANDLING: xdt99 extensions

       idt 'ASXERRS'

       ; includes and binary includes

txtinc copy  "nonexisting"    ;ERROR
bininc bcopy "nonexisting"    ;ERROR

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
       
       ; macros

       .defm mac1
       .endm
       .defm mac1             ;ERROR
       .endm     ; required, as assembly continues

       .defm mac2
       clr  #2                ;ERROR:0001
       .endm
       .mac2 1                ; error reported on actual line

       .macX                  ;ERROR

       .defm mac3
       .defm mac4             ;ERROR
       .endm

       ; weak symbols
w1:
       wequ 1
s2:
       equ 2
w1:
       equ 2                  ;ERROR
w1:
       equ 1                  ;OK
w1:
       equ 1                  ;ERROR

* NO ERRORS

good1:
       ; comment
       clr  0

       end
