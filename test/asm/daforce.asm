; re-assembly and force -F test

       aorg >a000

       clr  @>3000
l1     mov  @>8310, @>a820

l2     mov  @>8300, @>8380(r2)
       a    *r1+, @>2000

       b    @l2 - 2

       clr  @>3000
       clr  @>3100

       a    @>3000, @>4000
       end
