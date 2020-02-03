     def b1, b2, b3
     ref d1, d2, d3, x

     data 1, d1         ; no ref at addr 0!
b3   mov  @r2, @d2

     rorg

b1   equ  r3
     data d2
     data d3
     ai   r0, x

b2   end

