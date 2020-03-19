* write VDP register

       def  vwtr
       ref  vdpwa

       even

vwtr:
       data >2094
       data !vwtr

!vwtr:
       movb @1(r13), @vdpwa
       mov  *r13, r0
       ori  r0, >8000
       movb r0, @vdpwa

       rtwp
