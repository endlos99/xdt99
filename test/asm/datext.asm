       aorg >7000

       limi 0
       li   r0, t1
       bl   @write
       jmp  cont

       data >1000
t1     text 'BEISPIELTEXT?!'
       data >1000

cont   li   r0, t2
       bl   @write

       jmp  $

       data >1000
t2     text 'ABC:DEF-GHI,JKL. ?'
       data >1000

write:
       rt
       
       end
