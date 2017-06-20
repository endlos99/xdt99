       aorg >a000

start:
       limi 0
       lwpi >83e0
       li   r0, >1234
       bl   *r0
       data >ffaa
       swpb r15
       mov  r1, r2
       clr  @2(r3)
       szc  @>8300, r3

       end
