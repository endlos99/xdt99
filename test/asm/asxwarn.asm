* disable different categories of warnings

s0     equ  1
s1     data 0

sloop  clr  0
       mov  1, @2

       copy "asxwarni.asm"

send   b    @sloop

       end
