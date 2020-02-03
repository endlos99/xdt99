*  ERROR HANDLING: xdt99 extensions

       idt 'ASXERRS'

       ; include_path and binary include_path

txtinc copy  "nonexisting"    ;ERROR
bininc bcopy "nonexisting"    ;ERROR

       ; text bytes

text1  text >123456
       text >12x34            ;ERROR
       
       ; arg count

*      rtwp r1         ; cannt detect this: r1 is comment
*      nop @1          ; ditto
       inc r1, r2             ;ERROR
       byte                   ;ERROR
       text                   ;ERROR
       mov r1                 ;ERROR

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

       ; 9995 and F18A not available without -5 or -18

nnn    lst r0                 ;ERROR
       lwp r1                 ;ERROR
       divs r2                ;ERROR
       mpys *r3+              ;ERROR

       call *r1               ;ERROR
       push @nnn              ;ERROR
       pop r1                 ;ERROR
       slc r4, 9              ;ERROR

       ; hints for incorrect use
uuu    b   uuu                ;ERROR
       jmp @uuu               ;ERROR
       inc 9                  ;OK, is warning only

       ; auto-constants

       a   w#text1, 0         ;ERROR
       a   w#w#1, 0           ;ERROR
       a   b#1 + text1, 0     ;ERROR
       a   1 + w#1, 0         ;ERROR
       a   (w#1) + 1, 0       ;ERROR

* NO ERRORS

good1:
       ; comment
       clr  0

       end
