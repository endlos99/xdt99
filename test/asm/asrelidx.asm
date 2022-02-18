* relaxed indexed addresses

x    equ  >8300
work equ  >83e0

     ; indexes
     mov  @x+2, @x
     mov  @work ^ x, @x(r2)
     mov  @(work), @x+2(r2)
     c    @work * 2 ( r1 ), @>1000 ( :101 )
     ab   @work + (2 * x ^ >3000) (r9), @7643 | (x + 2) (>a)

     ; expressions
     c    @x & (2 * work + >4), @work ^ x + ~ (r1 + 4 )

     end
