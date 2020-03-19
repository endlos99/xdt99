* VDP multi-byte zero-terminated write

       def  vmzw
       ref  vdpwa, vdpwd

       even

vmzw:
       ori  r0, >4000
       swpb r0
       movb r0, @vdpwa
       swpb r0
       movb r0, @vdpwa
       jmp  !start

!loop  movb r0, @vdpwd
!start movb *r1+, r0
       jne  -!loop

       rt
