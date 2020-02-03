     def d1, d2, d3
     ref b1, b2, b3, x

d1   clr  r0
     b    @b1
     data b3
     ai   r0, x
     
d2   bss  32

     rorg
d3   equ  3
     mov  @b1, @b2
     dec  @b3

     end  d1
