* VDP multi-byte read, where length can be zero

       def  vmbr
       ref  vdpwa, vdprd

       even

vmbr:
       andi r0, >3fff
       swpb r0
       movb r0, @vdpwa
       swpb r0
       movb r0, @vdpwa

       jmp  !dec
!mov   movb @vdprd, *r1+
!dec   dec  r2
       joc  -!mov

       rt
