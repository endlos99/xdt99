* VDP multi-byte write, where length can be zero

       def  vmbw
       ref  vdpwa, vdpwd

       even

vmbw:
       data >2094
       data !vmbw

!vmbw:
       movb @1(r13), @vdpwa
       mov  *r13, r0
       ori  r0, >4000
       movb r0, @vdpwa
       mov  @2(r13), r1
       mov  @4(r13), r2

       jmp  !dec
!mov   movb *r1+, @vdpwd
!dec   dec  r2
       joc  -!mov

       rtwp
