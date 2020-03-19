* VDP single-byte write

       def  vsbw
       ref  vdpwa, vdpwd

       even

vsbw:
       ori  r0, >4000
       swpb r0
       movb r0, @vdpwa
       swpb r0
       movb r0, @vdpwa
       movb r1, @vdpwd

       rt
