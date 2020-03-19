* VDP single-byte write

       def  vsbw
       ref  vdpwa, vdpwd

       even

vsbw:
       data >2094
       data !vsbw

!vsbw:
       movb @1(r13), @vdpwa
       mov  *r13, r0
       ori  r0, >4000
       movb r0, @vdpwa
       movb @2(r13), @vdpwd

       rtwp
