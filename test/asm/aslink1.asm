     def d1, d2, d3
     def b1, b2, b3
     ref x

d1   clr  r0
     b    @b1
     data b3
     ai   r0, x

d2   bss  32

     rorg
d3   equ  3
     mov  @b1, @b2
     dec  @b3

     rorg

     data 1, d1
b3   mov  @r2, @d2

     rorg

b1   equ  r3
     data d2
     data d3
     ai   r0, x

b2   end  d1
