* relaxed indexed addresses (reference)

x    equ  >8300
work equ  >83e0

     ; indexes
     mov  @>8302, @>8300
     mov  @>e0, @>8300(r2)
     mov  @>83e0, @>8302(r2)
     c    @>07c0(r1), @>1000(r5)
     ab   @>b9e0(r9), @>9fdb(r10)

     ; expressions
     c    @>0300, @>00da

     end
