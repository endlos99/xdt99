* disassembly test program

       aorg >1000

       data >1000
       data >1000

return:
       rt

       data >1000
start:
       limi 0
       lwpi >8300

       bl   @return
       clr  @2(r1)
       c    r1, *r1+
       jeq  b1
       jmp  b2

       data >1000

b1:
       inc  @>8300
       bl   @s1
       mov  r1, r2
       jmp  start

       data >1000

b2:
       stwp r1
       ldcr r1, 5
       bl   @start

       b    @b1

       data >1000

other:
       li   r0, >1000
       bl   @s1
       li   r1, s2
       bl   *r1  ; won't work
       jmp  n1
       data >1000
n1:
       jmp  other

       data >1000

s1:
       a    *r1, @>8302(r2)
       rt

       data >1000

s2:
       data >1000  ; cannot reach this

       end
