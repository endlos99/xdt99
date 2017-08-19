       aorg >2000
ten:
       equ  >10
hundred:
       equ  >100

start  limi 0
       li   r0, ten
       mov  @start,@hundred(r1)
       jmp  start

       end
