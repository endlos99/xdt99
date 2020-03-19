* VDP write word text: write hex value of r1 to r0

       def  vwwt
       ref  vdpwa, vdpwd

       even

vwwt:
       ori  r0, >4000
       swpb r0
       movb r0, @vdpwa
       swpb r0
       movb r0, @vdpwa

       li   r0, 4             ; number of nybbles to show
       mov  r1, r2
       srl  r2, 4
       jmp  !
!next:
       mov  r1, r2            ; copy for printing
       sla  r1, 4             ; next nybble
!      andi r2, >0f00
       ai   r2, '0 '
       ci   r2, '9 '
       jle  !
       ai   r2, '@ ' - '9 '
!      movb r2, @vdpwd

       dec  r0
       jne  -!next

       rt
