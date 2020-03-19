* VDP multi-byte read, where length can be zero

       def  vmbr
       ref  vdpwa, vdprd

       even

vmbr:
       data >2094
       data !vmbr

!vmbr:
       movb @1(r13), @vdpwa
       mov  *r13, r0
       andi r0, >3fff
       movb r0, @vdpwa
       mov  @2(r13), r1
       mov  @4(r13), r2

       jmp  !dec
!mov   movb @vdprd, *r1+
!dec   dec  r2
       joc  -!mov

       rtwp
