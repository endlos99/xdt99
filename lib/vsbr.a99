* VDP single-byte write

       def  vsbr
       ref  vdpwa, vdprd

       even

vsbr:
       andi r0, >3fff
       swpb r0
       movb r0, @vdpwa
       swpb r0
       movb r0, @vdpwa
       movb @vdprd, r1

       rt
