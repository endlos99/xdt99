* TMS99000s extensions

dval:
       data >0012, >3456
sum:
       data >0000, >ffff

l1     am   r0, *r2+
       sm   @dval, @sum(r1)

       slam @dval, 17
       sram r2, 4

l2     bind @jmp(r1)
       li   r11, >83e0
       blsk r11, l3

l3     tmb  @>8300, 2
       tsmb r1, 0
       tcmb @sum(r1), 15

jmp:
       data l1, l2, l3

       end
