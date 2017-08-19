* disassembly test program

       data >1000

start:
       limi 0
       lwpi >8300

       clr  r1
!      movb @>837c, r1
       jeq  next
       dec  r2
       jne  -!
       jmp  next
       
       data >1000

next:
       bl   @blsub
       clr  @>8300(r2)
       mov  r1, r2
       blwp @blwpsub

       limi 2
       b    @start

       data >1000

blsub:
       a    r1, @>8302
       rt

       data >1000

blwpsub:
       data >83e0
       data blwpstart

       data >1000
blwpstart:
       mov  r11, *r1+
       rt

       data >1000

       end
