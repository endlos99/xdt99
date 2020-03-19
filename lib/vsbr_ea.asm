* VDP single-byte write

       def  vsbr
       ref  vdpwa, vdprd

       even

vsbr:
       data >2094
       data !vsbr

!vsbr:
       movb @1(r13), @vdpwa
       mov  *r13, r0
       andi r0, >3fff
       movb r0, @vdpwa
       movb @vdprd, @2(r13)

       rtwp
