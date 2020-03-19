* VDP single-byte multi-write

       def  vsbmw
       ref  vdpwa, vdpwd

       even

vsbmw:
       ori  r0, >4000
       swpb r0
       movb r0, @vdpwa
       swpb r0
       movb r0, @vdpwa

!      movb r1, @vdpwd
       dec  r2
       jne  -!

       rt
