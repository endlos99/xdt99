* symbols generation test

       ref  vdpwa, scan

s1:
       equ  1

start:
       limi 0
       li   r0, 1
       mov  r0, r1
       movb r2, @vdpwa

       bl   @s2

       limi 2
       jmp  $

s2:
       clr  r1
       blwp @scan
       rt

       end
