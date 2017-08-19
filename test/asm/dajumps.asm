* jump/origin tests

       limi 0
       lwpi >83e0

       clr  r0
s0:
       li   r1, s1
       bl   @sub

       jmp  s2

s1:
       text 'HELLOWORLD'
       data 0

s2:
       li   r1, s2
       bl   @sub
       inct r0
       b    @s0

sub:
       mov  *r1+, *r2+
       jne  sub
       rt

       end
