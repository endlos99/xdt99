* new EQU, WEQU semantics, errors

    aorg >2000

w1  wequ 1
w1  equ  2
w1  equ  3         ;ERROR

w2  equ  >2000
w2  clr  0         ;ERROR

w3  wequ >2002
w3  clr  0         ;ERROR

w4  clr  0
w4  equ  >2004     ;ERROR

w5  clr  0
w5  wequ >2006     ;ERROR

    end
